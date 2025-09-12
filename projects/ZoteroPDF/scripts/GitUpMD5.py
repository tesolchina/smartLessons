import os
import requests
import base64
import time
import json
import math
import shutil
from getpass import getpass
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm

class GitHubUploader:
    def __init__(self, repo_owner, repo_name, github_token, branch='main'):
        self.repo_owner = repo_owner
        self.repo_name = repo_name
        self.github_token = github_token
        self.branch = branch
        self.rate_limit_remaining = 5000
        self.rate_limit_reset = 0
        self.last_request_time = 0
        self.state_file = "upload_state.json"
        self.failed_uploads = self.load_state()
        self.max_files_per_dir = 999  # GitHub's limit before truncation

    def load_state(self):
        """Load previous failed uploads from state file"""
        try:
            if os.path.exists(self.state_file):
                with open(self.state_file, 'r') as f:
                    return json.load(f)
        except Exception:
            pass
        return []

    def save_state(self):
        """Save current state of failed uploads"""
        with open(self.state_file, 'w') as f:
            json.dump(self.failed_uploads, f)

    def organize_files_into_subdirs(self, local_directory):
        """
        Organize files into subdirectories with max_files_per_dir files each
        Returns the list of (local_path, repo_path) tuples
        """
        # Get all files from the directory
        all_files = [
            f for f in os.listdir(local_directory)
            if os.path.isfile(os.path.join(local_directory, f))
        ]
        
        # Create subdirectories if needed
        num_subdirs = math.ceil(len(all_files) / self.max_files_per_dir)
        if num_subdirs <= 1:
            return [
                (os.path.join(local_directory, f), f)
                for f in all_files
            ]
        
        print(f"\nOrganizing {len(all_files)} files into {num_subdirs} subdirectories...")
        
        # Create subdirectories and move files
        file_groups = []
        for i in range(num_subdirs):
            subdir_name = f"batch_{i+1:03d}"
            subdir_path = os.path.join(local_directory, subdir_name)
            os.makedirs(subdir_path, exist_ok=True)
            
            start_idx = i * self.max_files_per_dir
            end_idx = start_idx + self.max_files_per_dir
            batch_files = all_files[start_idx:end_idx]
            
            for file in batch_files:
                src = os.path.join(local_directory, file)
                dst = os.path.join(subdir_path, file)
                shutil.move(src, dst)
                
                repo_path = os.path.join(subdir_name, file).replace('\\', '/')
                file_groups.append((dst, repo_path))
        
        return file_groups

    def update_failed_uploads(self, local_path, repo_path, error):
        """Update the list of failed uploads"""
        entry = {
            'local_path': local_path,
            'repo_path': repo_path,
            'error': error,
            'timestamp': time.time()
        }
        existing = next((x for x in self.failed_uploads 
                        if x['local_path'] == local_path), None)
        if existing:
            existing.update(entry)
        else:
            self.failed_uploads.append(entry)
        self.save_state()

    def clear_successful_uploads(self, local_path):
        """Remove successfully uploaded files from failed list"""
        self.failed_uploads = [x for x in self.failed_uploads 
                             if x['local_path'] != local_path]
        self.save_state()

    def check_rate_limit(self):
        """Check and update rate limit status"""
        url = "https://api.github.com/rate_limit"
        headers = {
            "Authorization": f"token {self.github_token}",
            "Accept": "application/vnd.github.v3+json"
        }
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                data = response.json()
                core = data['resources']['core']
                self.rate_limit_remaining = core['remaining']
                self.rate_limit_reset = core['reset']
                print(f"\nRate limit: {self.rate_limit_remaining} remaining, resets at {time.ctime(self.rate_limit_reset)}")
        except Exception as e:
            print(f"Error checking rate limit: {e}")

    def wait_for_rate_limit(self):
        """Handle rate limit waiting"""
        now = time.time()
        
        if self.rate_limit_remaining <= 50:
            reset_time = max(0, self.rate_limit_reset - now)
            if reset_time > 0:
                print(f"\nApproaching rate limit. Waiting {math.ceil(reset_time)} seconds...")
                with tqdm(total=reset_time, desc="Waiting for rate limit reset") as pbar:
                    for _ in range(math.ceil(reset_time)):
                        time.sleep(1)
                        pbar.update(1)
                self.check_rate_limit()
        
        # Enforce minimum delay between requests
        min_delay = 1.0
        elapsed = now - self.last_request_time
        if elapsed < min_delay:
            time.sleep(min_delay - elapsed)
        
        self.last_request_time = time.time()

    def upload_file(self, local_path, repo_path, commit_message, force=False, max_retries=3):
        """Upload a single file with automatic failure tracking"""
        api_url = f"https://api.github.com/repos/{self.repo_owner}/{self.repo_name}/contents/{repo_path}"
        
        for attempt in range(max_retries):
            try:
                self.wait_for_rate_limit()
                
                with open(local_path, 'rb') as file:
                    content = base64.b64encode(file.read()).decode('utf-8')
                
                headers = {
                    "Authorization": f"token {self.github_token}",
                    "Accept": "application/vnd.github.v3+json"
                }
                
                response = requests.get(api_url, headers=headers)
                sha = None
                
                if response.status_code == 200:
                    existing_content = response.json().get('content', '')
                    if existing_content.replace('\n', '') == content.replace('\n', ''):
                        self.clear_successful_uploads(local_path)
                        return ('skipped', local_path, repo_path, "Content identical")
                    sha = response.json().get('sha')
                
                data = {
                    "message": commit_message,
                    "content": content,
                    "branch": self.branch
                }
                if sha and force:
                    data["sha"] = sha
                
                self.wait_for_rate_limit()
                response = requests.put(api_url, headers=headers, json=data)
                
                if response.status_code in [200, 201]:
                    self.rate_limit_remaining -= 1
                    self.clear_successful_uploads(local_path)
                    return ('success', local_path, repo_path, None)
                elif response.status_code == 409:
                    error_msg = response.json().get('message', '')
                    if 'is at' in error_msg and 'but expected' in error_msg:
                        latest_sha = error_msg.split('is at ')[1].split(' but')[0]
                        data['sha'] = latest_sha
                        continue
                    self.update_failed_uploads(local_path, repo_path, error_msg)
                    return ('failed', local_path, repo_path, error_msg)
                else:
                    error_msg = f"HTTP {response.status_code}: {response.json().get('message', 'No error message')}"
                    self.update_failed_uploads(local_path, repo_path, error_msg)
                    return ('failed', local_path, repo_path, error_msg)
            
            except Exception as e:
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)
                    continue
                self.update_failed_uploads(local_path, repo_path, str(e))
                return ('error', local_path, repo_path, str(e))
        
        error_msg = "Max retries exceeded"
        self.update_failed_uploads(local_path, repo_path, error_msg)
        return ('failed', local_path, repo_path, error_msg)

def main():
    print("GitHub Bulk File Upload Tool (With Subdirectory Splitting)")
    print("--------------------------------------------------------")
    
    # Configuration
    repo_owner = "ahmad-rev0"
    repo_name = "ZoteroMDsMineru3"
    local_directory = "D:\\mineru_mds_sorted_by_script"
    github_token = ""
    branch = "main"
    commit_message = "Upload files with subdirectory organization"
    max_workers = 2
    force = True
    
    # Initialize uploader
    uploader = GitHubUploader(repo_owner, repo_name, github_token, branch)
    uploader.check_rate_limit()
    
    # Check for previous failed uploads
    if uploader.failed_uploads:
        print(f"\nFound {len(uploader.failed_uploads)} previously failed uploads")
        retry_failed = input("Retry these failed uploads? (y/n): ").lower() == 'y'
        if retry_failed:
            files_to_upload = [
                (x['local_path'], x['repo_path']) 
                for x in uploader.failed_uploads
            ]
        else:
            uploader.failed_uploads = []
            files_to_upload = []
    else:
        files_to_upload = []
    
    # If no failed uploads or user chose not to retry, organize and gather new files
    if not files_to_upload:
        files_to_upload = uploader.organize_files_into_subdirs(local_directory)
    
    if not files_to_upload:
        print("No files found to upload!")
        return
    
    print(f"\nProcessing {len(files_to_upload)} files...")
    
    # Process files
    results = {
        'success': 0,
        'skipped': 0,
        'failed': 0,
        'error': 0
    }
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = []
        for local_path, repo_path in files_to_upload:
            futures.append(executor.submit(
                uploader.upload_file,
                local_path, repo_path, commit_message, force
            ))
        
        for future in tqdm(as_completed(futures), total=len(files_to_upload), desc="Uploading"):
            status, local_path, repo_path, error = future.result()
            results[status] += 1
    
    # Print summary
    print("\nUpload Summary:")
    for status, count in results.items():
        print(f"{status.capitalize()}: {count}")
    
    if results['failed'] > 0 or results['error'] > 0:
        print(f"\n{len(uploader.failed_uploads)} uploads failed and have been saved for next run")
        print("Failed files saved in 'upload_state.json'")
    
    print(f"\nFinal rate limit remaining: {uploader.rate_limit_remaining}")

if __name__ == "__main__":
    main()
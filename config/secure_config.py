"""
Secure configuration loader for DailyAssistant
Handles environment variables and secure credential management
"""

import os
import json
from pathlib import Path
from typing import Dict, Any, Optional

class SecureConfig:
    """Secure configuration manager for API credentials and sensitive data"""
    
    def __init__(self, env_file_path: Optional[str] = None):
        """
        Initialize secure config loader
        
        Args:
            env_file_path: Path to .env file (defaults to repo root)
        """
        self.repo_root = self._find_repo_root()
        if env_file_path:
            self.env_file = Path(env_file_path)
        else:
            self.env_file = self.repo_root / ".env"
        self._load_env_file()
    
    def _find_repo_root(self) -> Path:
        """Find the repository root directory"""
        current = Path(__file__).absolute()
        while current != current.parent:
            if (current / ".git").exists():
                return current
            current = current.parent
        # Fallback to current file's directory
        return Path(__file__).parent
    
    def _load_env_file(self) -> None:
        """Load environment variables from .env file"""
        if not self.env_file.exists():
            print(f"⚠️  No .env file found at {self.env_file}")
            print(f"📋 Copy .env.template to .env and fill in your credentials")
            return
        
        with open(self.env_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    # Remove quotes if present
                    value = value.strip('"\'')
                    os.environ[key] = value
    
    def get_google_credentials_dict(self, service: str = "docs") -> Dict[str, Any]:
        """
        Generate Google OAuth credentials dictionary from environment variables
        
        Args:
            service: Service type ("docs" or "slides")
            
        Returns:
            Dictionary in Google credentials.json format
        """
        prefix = f"GOOGLE_{service.upper()}_"
        
        client_id = os.getenv(f"{prefix}CLIENT_ID")
        client_secret = os.getenv(f"{prefix}CLIENT_SECRET") 
        project_id = os.getenv(f"{prefix}PROJECT_ID")
        
        if not all([client_id, client_secret, project_id]):
            missing = []
            if not client_id: missing.append(f"{prefix}CLIENT_ID")
            if not client_secret: missing.append(f"{prefix}CLIENT_SECRET")
            if not project_id: missing.append(f"{prefix}PROJECT_ID")
            
            raise ValueError(f"Missing required Google {service} credentials: {', '.join(missing)}")
        
        return {
            "installed": {
                "client_id": client_id,
                "project_id": project_id,
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                "client_secret": client_secret,
                "redirect_uris": ["http://localhost"]
            }
        }
    
    def create_temp_credentials_file(self, service: str = "docs") -> Path:
        """
        Create a temporary credentials.json file from environment variables
        
        Args:
            service: Service type ("docs" or "slides")
            
        Returns:
            Path to temporary credentials file
        """
        credentials_dict = self.get_google_credentials_dict(service)
        
        # Create temporary file in system temp directory
        import tempfile
        temp_dir = Path(tempfile.gettempdir()) / "dailyassistant_temp"
        temp_dir.mkdir(exist_ok=True)
        
        temp_file = temp_dir / f"credentials_{service}.json"
        
        with open(temp_file, 'w') as f:
            json.dump(credentials_dict, f, indent=2)
        
        return temp_file
    
    def get_api_key(self, service: str) -> str:
        """
        Get API key for a service
        
        Args:
            service: Service name (e.g., "openrouter")
            
        Returns:
            API key
        """
        key_name = f"{service.upper()}_API_KEY"
        api_key = os.getenv(key_name)
        
        if not api_key:
            raise ValueError(f"Missing API key: {key_name}")
        
        return api_key
    
    def cleanup_temp_files(self) -> None:
        """Remove temporary credential files"""
        import tempfile
        import shutil
        
        temp_dir = Path(tempfile.gettempdir()) / "dailyassistant_temp"
        if temp_dir.exists():
            shutil.rmtree(temp_dir)


# Global instance for easy access
config = SecureConfig()


def get_google_credentials_path(service: str = "docs") -> str:
    """
    Get path to Google credentials file (creates temporary file from env vars)
    
    Args:
        service: Service type ("docs" or "slides")
        
    Returns:
        Path to credentials file
    """
    return str(config.create_temp_credentials_file(service))


def get_api_key(service: str) -> str:
    """
    Get API key for a service
    
    Args:
        service: Service name
        
    Returns:
        API key
    """
    return config.get_api_key(service)


def cleanup_temp_credentials():
    """Clean up temporary credential files"""
    config.cleanup_temp_files()


# Example usage:
if __name__ == "__main__":
    try:
        # Test Google credentials
        creds_path = get_google_credentials_path("docs")
        print(f"✅ Google Docs credentials available at: {creds_path}")
        
        creds_path = get_google_credentials_path("slides") 
        print(f"✅ Google Slides credentials available at: {creds_path}")
        
        # Test API keys
        api_key = get_api_key("openrouter")
        print(f"✅ OpenRouter API key loaded (starts with: {api_key[:10]}...)")
        
    except ValueError as e:
        print(f"❌ Configuration error: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
    finally:
        cleanup_temp_credentials()
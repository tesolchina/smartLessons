#!/usr/bin/env python3
"""
Google Docs API Toolkit - Main Interface
A comprehensive command-line interface for all Google Docs operations.

Usage:
    python google_docs_toolkit.py read --doc-id YOUR_DOCUMENT_ID
    python google_docs_toolkit.py edit --url "https://docs.google.com/document/d/YOUR_ID/edit" --append "New content"
    python google_docs_toolkit.py comments --doc-id YOUR_DOCUMENT_ID --list-comments
    python google_docs_toolkit.py batch --doc-id YOUR_DOCUMENT_ID --read --add-feedback --append "Session complete"
"""

import sys
import os
import argparse
from datetime import datetime

# Add the current directory to Python path for imports
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)

try:
    from google_docs_reader import GoogleDocsReader
    from google_docs_editor import GoogleDocsEditor
    from google_docs_comments import GoogleDocsCommentManager
except ImportError as e:
    print(f"❌ Error importing Google Docs tools: {e}")
    print("📁 Please ensure all required files are in the same directory:")
    print("   - google_docs_reader.py")
    print("   - google_docs_editor.py") 
    print("   - google_docs_comments.py")
    print("   - credentials.json")
    sys.exit(1)

class GoogleDocsToolkit:
    def __init__(self):
        self.reader = GoogleDocsReader()
        self.editor = GoogleDocsEditor()
        self.comment_manager = GoogleDocsCommentManager()
    
    def extract_doc_id(self, doc_id=None, url=None):
        """Extract document ID from either direct ID or URL"""
        if url:
            return self.reader.extract_doc_id_from_url(url)
        elif doc_id:
            return doc_id
        else:
            raise ValueError("Either doc_id or url must be provided")
    
    def read_document(self, doc_id=None, url=None, verbose=True):
        """Read a document and return its content"""
        doc_id = self.extract_doc_id(doc_id, url)
        
        if verbose:
            print(f"📖 Reading document: {doc_id}")
        
        content = self.reader.read_document(doc_id)
        document_info = self.reader.get_document_info(doc_id)
        
        if verbose and document_info:
            print(f"📄 Title: {document_info.get('title', 'Untitled')}")
            print(f"📊 Content length: {len(content)} characters")
        
        return content, document_info
    
    def edit_document(self, doc_id=None, url=None, operations=None):
        """Perform editing operations on a document"""
        doc_id = self.extract_doc_id(doc_id, url)
        
        if not operations:
            print("⚠️  No editing operations specified")
            return False
        
        print(f"✏️  Editing document: {doc_id}")
        
        success_count = 0
        for operation in operations:
            try:
                op_type = operation.get('type')
                
                if op_type == 'append':
                    result = self.editor.append_text(doc_id, operation['text'])
                elif op_type == 'insert':
                    result = self.editor.insert_text(
                        doc_id, 
                        operation['text'], 
                        operation.get('index', 1)
                    )
                elif op_type == 'replace':
                    result = self.editor.replace_text(
                        doc_id,
                        operation['search_text'],
                        operation['replacement_text']
                    )
                elif op_type == 'format':
                    result = self.editor.add_formatted_text(
                        doc_id,
                        operation['text'],
                        operation.get('index', 1),
                        operation.get('style', {})
                    )
                else:
                    print(f"❌ Unknown operation type: {op_type}")
                    continue
                
                if result:
                    success_count += 1
                    print(f"✅ {op_type.capitalize()} operation completed")
                else:
                    print(f"❌ {op_type.capitalize()} operation failed")
                    
            except Exception as e:
                print(f"❌ Error in {op_type} operation: {e}")
        
        print(f"📊 Completed {success_count}/{len(operations)} operations")
        return success_count == len(operations)
    
    def manage_comments(self, doc_id=None, url=None, comment_operations=None):
        """Manage comments on a document"""
        doc_id = self.extract_doc_id(doc_id, url)
        
        if not comment_operations:
            print("⚠️  No comment operations specified")
            return False
        
        print(f"💬 Managing comments for document: {doc_id}")
        
        results = []
        for operation in comment_operations:
            try:
                op_type = operation.get('type')
                
                if op_type == 'list':
                    comments = self.comment_manager.list_comments(doc_id)
                    results.append({'type': 'list', 'comments': comments})
                
                elif op_type == 'add_general':
                    comment_id = self.comment_manager.add_general_comment(
                        doc_id, operation['text']
                    )
                    results.append({'type': 'add_general', 'comment_id': comment_id})
                
                elif op_type == 'add_anchored':
                    comment_id = self.comment_manager.add_anchored_comment(
                        doc_id,
                        operation['text'],
                        search_text=operation.get('anchor_text'),
                        position_start=operation.get('anchor_start'),
                        position_end=operation.get('anchor_end')
                    )
                    results.append({'type': 'add_anchored', 'comment_id': comment_id})
                
                elif op_type == 'add_feedback':
                    feedback_results = self.comment_manager.add_feedback_comments(
                        doc_id, operation.get('feedback_sections', {})
                    )
                    results.append({'type': 'add_feedback', 'results': feedback_results})
                
                elif op_type == 'resolve':
                    success = self.comment_manager.resolve_comment(
                        doc_id, operation['comment_id']
                    )
                    results.append({'type': 'resolve', 'success': success})
                
                elif op_type == 'delete':
                    success = self.comment_manager.delete_comment(
                        doc_id, operation['comment_id']
                    )
                    results.append({'type': 'delete', 'success': success})
                
                else:
                    print(f"❌ Unknown comment operation: {op_type}")
                    
            except Exception as e:
                print(f"❌ Error in {op_type} comment operation: {e}")
        
        return results
    
    def batch_operations(self, doc_id=None, url=None, operations=None):
        """Perform multiple operations in sequence"""
        doc_id = self.extract_doc_id(doc_id, url)
        
        if not operations:
            print("⚠️  No operations specified")
            return {}
        
        print(f"🔄 Starting batch operations on document: {doc_id}")
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        results = {
            'timestamp': timestamp,
            'document_id': doc_id,
            'operations_completed': []
        }
        
        for i, operation in enumerate(operations, 1):
            op_name = operation.get('name', f'Operation {i}')
            print(f"\\n📋 {i}/{len(operations)}: {op_name}")
            
            try:
                if operation['type'] == 'read':
                    content, doc_info = self.read_document(doc_id, verbose=False)
                    results['operations_completed'].append({
                        'name': op_name,
                        'type': 'read',
                        'success': True,
                        'content_length': len(content),
                        'title': doc_info.get('title', 'Untitled') if doc_info else 'Unknown'
                    })
                
                elif operation['type'] == 'edit':
                    edit_success = self.edit_document(doc_id, operations=operation['edit_operations'])
                    results['operations_completed'].append({
                        'name': op_name,
                        'type': 'edit',
                        'success': edit_success
                    })
                
                elif operation['type'] == 'comments':
                    comment_results = self.manage_comments(doc_id, comment_operations=operation['comment_operations'])
                    results['operations_completed'].append({
                        'name': op_name,
                        'type': 'comments',
                        'success': True,
                        'results': comment_results
                    })
                
                else:
                    print(f"❌ Unknown batch operation type: {operation['type']}")
                    results['operations_completed'].append({
                        'name': op_name,
                        'type': operation['type'],
                        'success': False,
                        'error': 'Unknown operation type'
                    })
                
            except Exception as e:
                print(f"❌ Error in {op_name}: {e}")
                results['operations_completed'].append({
                    'name': op_name,
                    'type': operation.get('type', 'unknown'),
                    'success': False,
                    'error': str(e)
                })
        
        successful_ops = sum(1 for op in results['operations_completed'] if op['success'])
        total_ops = len(results['operations_completed'])
        
        print(f"\\n📊 Batch operations complete: {successful_ops}/{total_ops} successful")
        results['summary'] = {
            'total_operations': total_ops,
            'successful_operations': successful_ops,
            'success_rate': f"{(successful_ops/total_ops)*100:.1f}%" if total_ops > 0 else "0%"
        }
        
        return results

def create_sample_config():
    """Create a sample configuration file for batch operations"""
    sample_config = {
        "document_id": "YOUR_DOCUMENT_ID_HERE",
        "operations": [
            {
                "name": "Read Document",
                "type": "read"
            },
            {
                "name": "Add Feedback Comments",
                "type": "comments",
                "comment_operations": [
                    {
                        "type": "add_feedback"
                    }
                ]
            },
            {
                "name": "Add Session Notes",
                "type": "edit",
                "edit_operations": [
                    {
                        "type": "append",
                        "text": "\\n\\n--- AI Assistant Session ---\\nReviewed and provided feedback on document structure and content.\\nTimestamp: {timestamp}\\n"
                    }
                ]
            }
        ]
    }
    
    import json
    with open(os.path.join(SCRIPT_DIR, 'sample_batch_config.json'), 'w') as f:
        json.dump(sample_config, f, indent=2)
    
    print("📝 Sample configuration created: sample_batch_config.json")

def main():
    parser = argparse.ArgumentParser(description='Google Docs Toolkit - Comprehensive document management')
    parser.add_argument('command', choices=['read', 'edit', 'comments', 'batch', 'config'], 
                       help='Command to execute')
    
    # Document identification
    parser.add_argument('--doc-id', help='Google Docs document ID')
    parser.add_argument('--url', help='Google Docs URL')
    
    # Read operations
    parser.add_argument('--info', action='store_true', help='Show document info')
    
    # Edit operations
    parser.add_argument('--append', help='Append text to document')
    parser.add_argument('--insert', help='Insert text at specified position')
    parser.add_argument('--insert-at', type=int, default=1, help='Position to insert text (default: 1)')
    parser.add_argument('--replace-text', help='Text to search for replacement')
    parser.add_argument('--replacement', help='Replacement text')
    
    # Comment operations
    parser.add_argument('--list-comments', action='store_true', help='List all comments')
    parser.add_argument('--add-comment', help='Add a general comment')
    parser.add_argument('--add-feedback', action='store_true', help='Add standard feedback comments')
    
    # Batch operations
    parser.add_argument('--config-file', help='JSON configuration file for batch operations')
    
    args = parser.parse_args()
    
    if args.command == 'config':
        create_sample_config()
        return
    
    if not args.doc_id and not args.url:
        print("❌ Please provide either --doc-id or --url")
        sys.exit(1)
    
    toolkit = GoogleDocsToolkit()
    
    try:
        if args.command == 'read':
            content, doc_info = toolkit.read_document(args.doc_id, args.url)
            
            if args.info and doc_info:
                print("\\n📋 Document Information:")
                print(f"  Title: {doc_info.get('title', 'Untitled')}")
                print(f"  Document ID: {doc_info.get('documentId', 'Unknown')}")
                print(f"  Created: {doc_info.get('createdTime', 'Unknown')}")
                print(f"  Modified: {doc_info.get('modifiedTime', 'Unknown')}")
            
            print("\\n📄 Document Content:")
            print("="*60)
            print(content)
        
        elif args.command == 'edit':
            operations = []
            
            if args.append:
                operations.append({'type': 'append', 'text': args.append})
            
            if args.insert:
                operations.append({
                    'type': 'insert', 
                    'text': args.insert, 
                    'index': args.insert_at
                })
            
            if args.replace_text and args.replacement:
                operations.append({
                    'type': 'replace',
                    'search_text': args.replace_text,
                    'replacement_text': args.replacement
                })
            
            if operations:
                toolkit.edit_document(args.doc_id, args.url, operations)
            else:
                print("❌ No edit operations specified")
        
        elif args.command == 'comments':
            comment_operations = []
            
            if args.list_comments:
                comment_operations.append({'type': 'list'})
            
            if args.add_comment:
                comment_operations.append({'type': 'add_general', 'text': args.add_comment})
            
            if args.add_feedback:
                comment_operations.append({'type': 'add_feedback'})
            
            if comment_operations:
                toolkit.manage_comments(args.doc_id, args.url, comment_operations)
            else:
                print("❌ No comment operations specified")
        
        elif args.command == 'batch':
            if args.config_file:
                import json
                with open(args.config_file, 'r') as f:
                    config = json.load(f)
                
                doc_id = config.get('document_id', args.doc_id)
                operations = config.get('operations', [])
                
                # Process timestamp placeholders
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                for operation in operations:
                    if operation.get('type') == 'edit':
                        for edit_op in operation.get('edit_operations', []):
                            if 'text' in edit_op:
                                edit_op['text'] = edit_op['text'].replace('{timestamp}', timestamp)
                
                results = toolkit.batch_operations(doc_id, operations=operations)
                
                # Save results
                results_file = f"batch_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                with open(results_file, 'w') as f:
                    json.dump(results, f, indent=2)
                print(f"📊 Results saved to: {results_file}")
                
            else:
                print("❌ Please provide --config-file for batch operations")
                print("💡 Use 'python google_docs_toolkit.py config' to create a sample configuration")
    
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
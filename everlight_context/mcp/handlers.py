"""
handlers.py

MCP request handlers for the Aetherius Archive.
Implements specific handlers for tools, resources, and context management.
"""

from typing import Any, Dict, List, Optional
import os
from ..loader import load_documents, scan_logs_dir
from ..parser import parse_document
from ..models import DocumentProcessor


class ContextHandler:
    """
    Handles context requests for the Aetherius Archive.
    Provides archive state and metadata to MCP clients.
    """
    
    def __init__(self, logs_dir: str = "everlight_context/logs/"):
        """
        Initialize the context handler.
        
        Args:
            logs_dir: Directory containing archive documents
        """
        self.logs_dir = logs_dir
    
    def get_context(self, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Get current archive context.
        
        Args:
            params: Optional parameters for context request
            
        Returns:
            Dictionary containing archive context
        """
        files = scan_logs_dir(self.logs_dir)
        
        return {
            'archive_name': 'EverLight Aetherius Archive',
            'document_count': len(files),
            'logs_directory': self.logs_dir,
            'available_extensions': ['.html', '.md', '.txt'],
            'status': 'operational'
        }


class ToolHandler:
    """
    Handles tool execution requests for the Aetherius Archive.
    Provides access to document processing and search capabilities.
    """
    
    def __init__(self, logs_dir: str = "everlight_context/logs/"):
        """
        Initialize the tool handler.
        
        Args:
            logs_dir: Directory containing archive documents
        """
        self.logs_dir = logs_dir
        self.processor = DocumentProcessor()
        self.processor.initialize()
    
    def list_documents(self) -> List[Dict[str, str]]:
        """
        List all documents in the archive.
        
        Returns:
            List of document information dictionaries
        """
        files = scan_logs_dir(self.logs_dir)
        documents = []
        
        for filepath in files:
            filename = os.path.basename(filepath)
            documents.append({
                'filename': filename,
                'path': filepath
            })
        
        return documents
    
    def get_document(self, filename: str) -> Dict[str, Any]:
        """
        Get a specific document by filename.
        
        Args:
            filename: Name of the document to retrieve
            
        Returns:
            Dictionary containing document data
        """
        filepath = os.path.join(self.logs_dir, filename)
        
        if not os.path.exists(filepath):
            return {'error': f'Document not found: {filename}'}
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Process document
            result = self.processor.process({
                'filename': filename,
                'content': content
            })
            
            return result
        except Exception as e:
            return {'error': f'Error reading document: {str(e)}'}
    
    def search_documents(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Search for documents similar to the query.
        
        Args:
            query: Search query text
            top_k: Number of results to return
            
        Returns:
            List of similar documents
        """
        # First, ensure all documents are processed
        docs = load_documents(self.logs_dir)
        for filename, content in docs:
            if not self.processor.get_cached_document(filename):
                self.processor.process({
                    'filename': filename,
                    'content': content
                })
        
        # Perform search
        results = self.processor.search_similar_documents(query, top_k)
        return results
    
    def summarize_document(self, filename: str) -> Dict[str, str]:
        """
        Generate a summary of a document.
        
        Args:
            filename: Name of the document to summarize
            
        Returns:
            Dictionary containing the summary
        """
        doc_data = self.get_document(filename)
        
        if 'error' in doc_data:
            return doc_data
        
        return {
            'filename': filename,
            'summary': doc_data.get('summary', ''),
            'word_count': doc_data.get('word_count', 0)
        }


class ResourceHandler:
    """
    Handles resource requests for the Aetherius Archive.
    Provides access to archive documents as resources.
    """
    
    def __init__(self, logs_dir: str = "everlight_context/logs/"):
        """
        Initialize the resource handler.
        
        Args:
            logs_dir: Directory containing archive documents
        """
        self.logs_dir = logs_dir
    
    def get_document_resource(self, filename: str) -> str:
        """
        Get document content as a resource.
        
        Args:
            filename: Name of the document
            
        Returns:
            Document content as string
        """
        filepath = os.path.join(self.logs_dir, filename)
        
        if not os.path.exists(filepath):
            return f"Error: Document not found: {filename}"
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            return f"Error reading document: {str(e)}"
    
    def get_archive_index(self) -> str:
        """
        Get an index of all archive documents.
        
        Returns:
            Formatted string containing archive index
        """
        files = scan_logs_dir(self.logs_dir)
        
        index_lines = [
            "📚 EverLight Aetherius Archive Index",
            "=" * 50,
            ""
        ]
        
        for filepath in files:
            filename = os.path.basename(filepath)
            file_size = os.path.getsize(filepath)
            index_lines.append(f"📄 {filename} ({file_size} bytes)")
        
        index_lines.append("")
        index_lines.append(f"Total documents: {len(files)}")
        
        return "\n".join(index_lines)

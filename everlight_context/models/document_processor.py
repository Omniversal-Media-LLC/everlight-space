"""
document_processor.py

Document processing model for the Aetherius Archive.
Handles document analysis, summarization, and semantic extraction.
"""

from typing import Dict, List, Optional, Any
from .base_model import BaseAetheriusModel
from .embeddings import EmbeddingModel


# Constants for summarization
SENTENCE_TERMINATORS = ['. ', '! ', '? ']
MIN_SUMMARY_LENGTH_RATIO = 0.5  # Minimum ratio for sentence boundary detection


class DocumentProcessor(BaseAetheriusModel):
    """
    Advanced document processor for the Aetherius Archive.
    
    Analyzes archive documents to extract meaning, generate summaries,
    and prepare content for mythic understanding and retrieval.
    """
    
    def __init__(self, model_name: str = "aetherius-doc-processor",
                 use_embeddings: bool = True,
                 config: Optional[Dict[str, Any]] = None):
        """
        Initialize the document processor.
        
        Args:
            model_name: Name of the processor model
            use_embeddings: Whether to generate embeddings for documents
            config: Optional configuration parameters
        """
        super().__init__(model_name, config)
        self.use_embeddings = use_embeddings
        self.embedding_model = None
        self.document_cache = {}
    
    def initialize(self) -> bool:
        """
        Initialize the document processor and its dependencies.
        
        Returns:
            bool: True if initialization successful
        """
        try:
            if self.use_embeddings:
                self.embedding_model = EmbeddingModel()
                self.embedding_model.initialize()
            
            self._initialized = True
            return True
        except Exception as e:
            print(f"⚠️ Error initializing document processor: {e}")
            return False
    
    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process a document through the Archive's understanding.
        
        Args:
            input_data: Dictionary containing:
                - 'filename': Name of the document
                - 'content': Text content of the document
                - 'metadata': Optional metadata dictionary
            
        Returns:
            Dictionary containing processed document data:
                - 'filename': Original filename
                - 'summary': Generated summary
                - 'word_count': Number of words
                - 'embedding': Vector embedding (if enabled)
                - 'metadata': Enhanced metadata
        """
        if not self._initialized:
            self.initialize()
        
        filename = input_data.get('filename', 'unknown')
        content = input_data.get('content', '')
        metadata = input_data.get('metadata', {})
        
        # Generate comprehensive analysis
        result = {
            'filename': filename,
            'summary': self._generate_summary(content),
            'word_count': self._count_words(content),
            'char_count': len(content),
            'metadata': metadata
        }
        
        # Add embedding if enabled
        if self.use_embeddings and self.embedding_model:
            result['embedding'] = self.embedding_model.process(content)[0]
        
        # Cache processed document
        self.document_cache[filename] = result
        
        return result
    
    def _generate_summary(self, content: str, max_length: int = 200) -> str:
        """
        Generate a summary of the document content.
        
        Args:
            content: Document text content
            max_length: Maximum length of summary
            
        Returns:
            Summary string
        """
        # Enhanced summarization - takes first meaningful content
        summary = content.strip()[:max_length]
        
        # Clean up summary
        summary = summary.replace('\n', ' ').replace('\r', ' ')
        summary = ' '.join(summary.split())  # Normalize whitespace
        
        if len(content) > max_length:
            # Try to end at a sentence boundary
            for punct in SENTENCE_TERMINATORS:
                last_punct = summary.rfind(punct)
                if last_punct > max_length * MIN_SUMMARY_LENGTH_RATIO:
                    summary = summary[:last_punct + 1]
                    break
            else:
                summary += "..."
        
        return summary
    
    def _count_words(self, content: str) -> int:
        """
        Count words in the document.
        
        Args:
            content: Document text content
            
        Returns:
            Number of words
        """
        return len(content.split())
    
    def process_batch(self, documents: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Process multiple documents in batch.
        
        Args:
            documents: List of document dictionaries
            
        Returns:
            List of processed document results
        """
        return [self.process(doc) for doc in documents]
    
    def get_cached_document(self, filename: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve a previously processed document from cache.
        
        Args:
            filename: Name of the document to retrieve
            
        Returns:
            Cached document data or None if not found
        """
        return self.document_cache.get(filename)
    
    def search_similar_documents(self, query_text: str, 
                                top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Find documents similar to the query text.
        
        Args:
            query_text: Text to search for
            top_k: Number of results to return
            
        Returns:
            List of similar documents with similarity scores
        """
        if not self.use_embeddings or not self.embedding_model:
            return []
        
        # Generate query embedding
        query_embedding = self.embedding_model.process(query_text)[0]
        
        # Get embeddings from cached documents
        cached_docs = list(self.document_cache.values())
        if not cached_docs:
            return []
        
        # Filter documents that have embeddings
        docs_with_embeddings = [
            doc for doc in cached_docs 
            if 'embedding' in doc
        ]
        
        if not docs_with_embeddings:
            return []
        
        # Compute similarities
        results = []
        for doc in docs_with_embeddings:
            similarity = self.embedding_model.compute_similarity(
                query_embedding, 
                doc['embedding']
            )
            results.append({
                'filename': doc['filename'],
                'summary': doc['summary'],
                'similarity': float(similarity)
            })
        
        # Sort by similarity and return top_k
        results.sort(key=lambda x: x['similarity'], reverse=True)
        return results[:top_k]

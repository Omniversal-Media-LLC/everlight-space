"""
models/__init__.py

Model development module for the EverLight Aetherius Archive.
Provides base model classes, embedding support, and training utilities
for document processing and semantic understanding.
"""

from .base_model import BaseAetheriusModel
from .embeddings import EmbeddingModel
from .document_processor import DocumentProcessor

__all__ = [
    'BaseAetheriusModel',
    'EmbeddingModel',
    'DocumentProcessor',
]

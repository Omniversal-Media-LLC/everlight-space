"""
api/__init__.py

API integration module for the EverLight Aetherius Archive.
Provides connectivity to external services like Nextcloud Assistant.
"""

from .nextcloud_client import NextcloudAssistantClient
from .config import APIConfig

__all__ = [
    'NextcloudAssistantClient',
    'APIConfig',
]

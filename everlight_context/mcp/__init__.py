"""
mcp/__init__.py

Model Context Protocol (MCP) server implementation for EverLight Aetherius Archive.
Enables standardized API access to Archive models and context for AI assistants.
"""

from .server import MCPServer
from .handlers import ContextHandler, ToolHandler, ResourceHandler

__all__ = [
    'MCPServer',
    'ContextHandler',
    'ToolHandler',
    'ResourceHandler',
]

"""
server.py

MCP Server implementation for the Aetherius Archive.
Provides standardized Model Context Protocol interface for AI assistants.
"""

from typing import Any, Dict, List, Optional, Callable
import json
import asyncio
from datetime import datetime


# JSON-RPC 2.0 Error Codes
JSONRPC_METHOD_NOT_FOUND = -32601
JSONRPC_INTERNAL_ERROR = -32603


class MCPServer:
    """
    Model Context Protocol server for the EverLight Aetherius Archive.
    
    Implements the MCP specification to expose Archive capabilities
    to AI assistants like Nextcloud Assistant, Claude, or other MCP clients.
    """
    
    def __init__(self, name: str = "everlight-aetherius-archive",
                 version: str = "1.0.0",
                 config: Optional[Dict[str, Any]] = None):
        """
        Initialize the MCP server.
        
        Args:
            name: Server name identifier
            version: Server version
            config: Optional configuration dictionary
        """
        self.name = name
        self.version = version
        self.config = config or {}
        self.tools = {}
        self.resources = {}
        self.context_handlers = []
        self._running = False
    
    def register_tool(self, name: str, handler: Callable, 
                     description: str, parameters: Dict[str, Any]) -> None:
        """
        Register a tool that can be invoked by MCP clients.
        
        Args:
            name: Tool name/identifier
            handler: Function to call when tool is invoked
            description: Human-readable tool description
            parameters: JSON schema for tool parameters
        """
        self.tools[name] = {
            'handler': handler,
            'description': description,
            'parameters': parameters
        }
    
    def register_resource(self, uri: str, handler: Callable,
                         name: str, description: str) -> None:
        """
        Register a resource that can be accessed by MCP clients.
        
        Args:
            uri: Resource URI identifier
            handler: Function to fetch resource content
            name: Resource name
            description: Resource description
        """
        self.resources[uri] = {
            'handler': handler,
            'name': name,
            'description': description
        }
    
    def register_context_handler(self, handler: Callable) -> None:
        """
        Register a handler for context management.
        
        Args:
            handler: Function to handle context requests
        """
        self.context_handlers.append(handler)
    
    async def handle_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle an incoming MCP request.
        
        Args:
            request: MCP request dictionary
            
        Returns:
            MCP response dictionary
        """
        method = request.get('method')
        params = request.get('params', {})
        request_id = request.get('id')
        
        try:
            if method == 'initialize':
                result = await self._handle_initialize(params)
            elif method == 'tools/list':
                result = await self._handle_list_tools()
            elif method == 'tools/call':
                result = await self._handle_call_tool(params)
            elif method == 'resources/list':
                result = await self._handle_list_resources()
            elif method == 'resources/read':
                result = await self._handle_read_resource(params)
            elif method == 'context/get':
                result = await self._handle_get_context(params)
            else:
                return {
                    'jsonrpc': '2.0',
                    'id': request_id,
                    'error': {
                        'code': JSONRPC_METHOD_NOT_FOUND,
                        'message': f'Method not found: {method}'
                    }
                }
            
            return {
                'jsonrpc': '2.0',
                'id': request_id,
                'result': result
            }
        
        except Exception as e:
            return {
                'jsonrpc': '2.0',
                'id': request_id,
                'error': {
                    'code': JSONRPC_INTERNAL_ERROR,
                    'message': f'Internal error: {str(e)}'
                }
            }
    
    async def _handle_initialize(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle initialization request."""
        return {
            'protocolVersion': '1.0',
            'serverInfo': {
                'name': self.name,
                'version': self.version
            },
            'capabilities': {
                'tools': {'enabled': True},
                'resources': {'enabled': True},
                'context': {'enabled': True}
            }
        }
    
    async def _handle_list_tools(self) -> Dict[str, Any]:
        """List available tools."""
        tools_list = []
        for name, tool in self.tools.items():
            tools_list.append({
                'name': name,
                'description': tool['description'],
                'inputSchema': tool['parameters']
            })
        return {'tools': tools_list}
    
    async def _handle_call_tool(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a tool."""
        tool_name = params.get('name')
        arguments = params.get('arguments', {})
        
        if tool_name not in self.tools:
            raise ValueError(f"Tool not found: {tool_name}")
        
        tool = self.tools[tool_name]
        handler = tool['handler']
        
        # Execute tool handler
        if asyncio.iscoroutinefunction(handler):
            result = await handler(**arguments)
        else:
            result = handler(**arguments)
        
        return {
            'content': [
                {
                    'type': 'text',
                    'text': json.dumps(result, indent=2)
                }
            ]
        }
    
    async def _handle_list_resources(self) -> Dict[str, Any]:
        """List available resources."""
        resources_list = []
        for uri, resource in self.resources.items():
            resources_list.append({
                'uri': uri,
                'name': resource['name'],
                'description': resource['description']
            })
        return {'resources': resources_list}
    
    async def _handle_read_resource(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Read a resource."""
        uri = params.get('uri')
        
        if uri not in self.resources:
            raise ValueError(f"Resource not found: {uri}")
        
        resource = self.resources[uri]
        handler = resource['handler']
        
        # Execute resource handler
        if asyncio.iscoroutinefunction(handler):
            content = await handler()
        else:
            content = handler()
        
        return {
            'contents': [
                {
                    'uri': uri,
                    'mimeType': 'text/plain',
                    'text': content
                }
            ]
        }
    
    async def _handle_get_context(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Get context information."""
        context_data = {}
        
        for handler in self.context_handlers:
            if asyncio.iscoroutinefunction(handler):
                data = await handler(params)
            else:
                data = handler(params)
            context_data.update(data)
        
        return context_data
    
    def start(self, host: str = '0.0.0.0', port: int = 8080):
        """
        Start the MCP server.
        
        Args:
            host: Host address to bind to
            port: Port number to listen on
        """
        self._running = True
        print(f"🔮 EverLight MCP Server starting on {host}:{port}")
        print(f"📚 Archive: {self.name} v{self.version}")
        print(f"⚡ Tools registered: {len(self.tools)}")
        print(f"📖 Resources registered: {len(self.resources)}")
    
    def stop(self):
        """Stop the MCP server."""
        self._running = False
        print("🌙 EverLight MCP Server shutting down...")
    
    def is_running(self) -> bool:
        """Check if server is running."""
        return self._running

"""
mcp_server.py

MCP Server entry point for the EverLight Aetherius Archive.
Starts an MCP server that exposes Archive capabilities to AI assistants.
"""

import argparse
import asyncio
from everlight_context.mcp import MCPServer
from everlight_context.mcp.handlers import ContextHandler, ToolHandler, ResourceHandler
from everlight_context.api import APIConfig


def setup_server(config: APIConfig, logs_dir: str) -> MCPServer:
    """
    Set up and configure the MCP server with handlers.
    
    Args:
        config: API configuration
        logs_dir: Directory containing archive documents
        
    Returns:
        Configured MCPServer instance
    """
    server = MCPServer(
        name="everlight-aetherius-archive",
        version="1.0.0"
    )
    
    # Initialize handlers
    context_handler = ContextHandler(logs_dir)
    tool_handler = ToolHandler(logs_dir)
    resource_handler = ResourceHandler(logs_dir)
    
    # Register context handler
    server.register_context_handler(context_handler.get_context)
    
    # Register tools
    server.register_tool(
        name="list_documents",
        handler=tool_handler.list_documents,
        description="List all documents in the Aetherius Archive",
        parameters={
            "type": "object",
            "properties": {},
            "required": []
        }
    )
    
    server.register_tool(
        name="get_document",
        handler=tool_handler.get_document,
        description="Retrieve a specific document from the Archive",
        parameters={
            "type": "object",
            "properties": {
                "filename": {
                    "type": "string",
                    "description": "Name of the document to retrieve"
                }
            },
            "required": ["filename"]
        }
    )
    
    server.register_tool(
        name="search_documents",
        handler=tool_handler.search_documents,
        description="Search for documents similar to a query",
        parameters={
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Search query text"
                },
                "top_k": {
                    "type": "integer",
                    "description": "Number of results to return",
                    "default": 5
                }
            },
            "required": ["query"]
        }
    )
    
    server.register_tool(
        name="summarize_document",
        handler=tool_handler.summarize_document,
        description="Generate a summary of a document",
        parameters={
            "type": "object",
            "properties": {
                "filename": {
                    "type": "string",
                    "description": "Name of the document to summarize"
                }
            },
            "required": ["filename"]
        }
    )
    
    # Register resources
    server.register_resource(
        uri="archive://index",
        handler=resource_handler.get_archive_index,
        name="Archive Index",
        description="Complete index of all Archive documents"
    )
    
    # Register dynamic document resources
    for doc in tool_handler.list_documents():
        filename = doc['filename']
        server.register_resource(
            uri=f"archive://documents/{filename}",
            handler=lambda f=filename: resource_handler.get_document_resource(f),
            name=f"Document: {filename}",
            description=f"Content of {filename} from the Archive"
        )
    
    return server


async def run_server(server: MCPServer, host: str, port: int):
    """
    Run the MCP server (async version).
    
    Args:
        server: Configured MCP server
        host: Host address
        port: Port number
    """
    server.start(host, port)
    
    # Keep server running
    try:
        while server.is_running():
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        server.stop()


def main():
    """Main entry point for MCP server."""
    parser = argparse.ArgumentParser(
        description="EverLight Aetherius Archive MCP Server"
    )
    parser.add_argument(
        '--config',
        type=str,
        help='Path to configuration file'
    )
    parser.add_argument(
        '--host',
        type=str,
        default='0.0.0.0',
        help='Host address to bind to (default: 0.0.0.0)'
    )
    parser.add_argument(
        '--port',
        type=int,
        default=8080,
        help='Port number to listen on (default: 8080)'
    )
    parser.add_argument(
        '--logs-dir',
        type=str,
        default='everlight_context/logs/',
        help='Directory containing archive documents'
    )
    
    args = parser.parse_args()
    
    # Load configuration
    config = APIConfig(args.config)
    
    # Override with command line args
    host = args.host or config.get('mcp.host', '0.0.0.0')
    port = args.port or config.get('mcp.port', 8080)
    
    # Set up server
    server = setup_server(config, args.logs_dir)
    
    # Run server
    print("🔮 Starting EverLight Aetherius Archive MCP Server...")
    print(f"📍 Listening on {host}:{port}")
    print(f"📚 Archive directory: {args.logs_dir}")
    print("\nPress Ctrl+C to stop the server\n")
    
    try:
        asyncio.run(run_server(server, host, port))
    except KeyboardInterrupt:
        print("\n🌙 Server stopped by user")


if __name__ == "__main__":
    main()

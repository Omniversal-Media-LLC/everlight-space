#!/usr/bin/env python3
"""
example_usage.py

Demonstrates usage of the EverLight Aetherius Archive model development
infrastructure and MCP server integration.
"""

import asyncio
from everlight_context.models import DocumentProcessor
from everlight_context.mcp import MCPServer
from everlight_context.mcp.handlers import ContextHandler, ToolHandler, ResourceHandler
from everlight_context.api import NextcloudAssistantClient, APIConfig


def example_1_document_processing():
    """Example 1: Process documents with the DocumentProcessor."""
    print("=" * 60)
    print("📚 Example 1: Document Processing")
    print("=" * 60)
    
    # Initialize processor
    processor = DocumentProcessor(use_embeddings=True)
    processor.initialize()
    
    # Process a sample document
    doc = {
        'filename': 'mystical_knowledge.txt',
        'content': '''
        The EverLight Aetherius Archive stands as a beacon of knowledge across the Omniverse.
        Within its halls, countless documents chronicle the adventures, wisdom, and mysteries
        of countless realms. The Archive remembers all, preserving context and meaning for
        future generations of Archivists who seek understanding.
        ''',
        'metadata': {
            'author': 'Chief Archivist',
            'category': 'lore'
        }
    }
    
    result = processor.process(doc)
    
    print(f"\n📄 Document: {result['filename']}")
    print(f"📊 Word count: {result['word_count']}")
    print(f"📝 Summary: {result['summary']}")
    print(f"✨ Embedding shape: {result['embedding'].shape}")
    
    # Process another document and search
    doc2 = {
        'filename': 'archive_guide.txt',
        'content': 'A guide to navigating the Archive and understanding its mystical properties.'
    }
    processor.process(doc2)
    
    # Search for similar documents
    print("\n🔍 Searching for documents about 'Archive mysteries'...")
    search_results = processor.search_similar_documents("Archive mysteries", top_k=2)
    
    for i, result in enumerate(search_results, 1):
        print(f"\n  {i}. {result['filename']} (similarity: {result['similarity']:.3f})")
        print(f"     {result['summary'][:80]}...")


def example_2_mcp_server_setup():
    """Example 2: Set up an MCP server."""
    print("\n\n" + "=" * 60)
    print("🔮 Example 2: MCP Server Setup")
    print("=" * 60)
    
    # Create server
    server = MCPServer(
        name="everlight-aetherius-archive",
        version="1.0.0"
    )
    
    # Initialize handlers
    context_handler = ContextHandler("everlight_context/logs/")
    tool_handler = ToolHandler("everlight_context/logs/")
    resource_handler = ResourceHandler("everlight_context/logs/")
    
    # Register context handler
    server.register_context_handler(context_handler.get_context)
    
    # Register tools
    server.register_tool(
        name="list_documents",
        handler=tool_handler.list_documents,
        description="List all documents in the Archive",
        parameters={"type": "object", "properties": {}}
    )
    
    server.register_tool(
        name="search_documents",
        handler=tool_handler.search_documents,
        description="Search for documents",
        parameters={
            "type": "object",
            "properties": {
                "query": {"type": "string"},
                "top_k": {"type": "integer"}
            },
            "required": ["query"]
        }
    )
    
    # Register resource
    server.register_resource(
        uri="archive://index",
        handler=resource_handler.get_archive_index,
        name="Archive Index",
        description="Complete index of Archive documents"
    )
    
    print(f"\n✅ Server initialized: {server.name} v{server.version}")
    print(f"⚡ Tools registered: {len(server.tools)}")
    print(f"📖 Resources registered: {len(server.resources)}")
    print(f"\nRegistered tools:")
    for tool_name in server.tools.keys():
        print(f"  - {tool_name}")


async def example_3_mcp_request_handling():
    """Example 3: Handle MCP requests."""
    print("\n\n" + "=" * 60)
    print("📨 Example 3: MCP Request Handling")
    print("=" * 60)
    
    # Create and set up server
    server = MCPServer(name="test-server")
    
    def simple_tool(message: str):
        return {"echo": f"Archive says: {message}"}
    
    server.register_tool(
        name="echo",
        handler=simple_tool,
        description="Echo a message",
        parameters={
            "type": "object",
            "properties": {"message": {"type": "string"}},
            "required": ["message"]
        }
    )
    
    # Simulate an initialize request
    init_request = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "initialize",
        "params": {}
    }
    
    response = await server.handle_request(init_request)
    print(f"\n📥 Initialize Request")
    print(f"Response: {response['result']['serverInfo']}")
    
    # Simulate a tool list request
    list_request = {
        "jsonrpc": "2.0",
        "id": 2,
        "method": "tools/list",
        "params": {}
    }
    
    response = await server.handle_request(list_request)
    print(f"\n📥 List Tools Request")
    print(f"Available tools: {len(response['result']['tools'])}")
    for tool in response['result']['tools']:
        print(f"  - {tool['name']}: {tool['description']}")
    
    # Simulate a tool call
    call_request = {
        "jsonrpc": "2.0",
        "id": 3,
        "method": "tools/call",
        "params": {
            "name": "echo",
            "arguments": {"message": "Hello from the Aetherius Archive!"}
        }
    }
    
    response = await server.handle_request(call_request)
    print(f"\n📥 Tool Call Request")
    print(f"Result: {response['result']['content'][0]['text']}")


def example_4_nextcloud_client():
    """Example 4: Nextcloud Assistant client setup."""
    print("\n\n" + "=" * 60)
    print("☁️  Example 4: Nextcloud Assistant Integration")
    print("=" * 60)
    
    # Load configuration
    config = APIConfig()
    
    # Set up client (using example values)
    client = NextcloudAssistantClient(
        base_url="https://your-nextcloud.example.com",
        username="archivist",
        app_password="your-app-password"
    )
    
    print(f"\n✅ Nextcloud client initialized")
    print(f"🔗 Base URL: {client.base_url}")
    
    # Test connection
    connection_test = client.test_connection()
    print(f"\n🔌 Connection test:")
    print(f"  Status: {connection_test['message']}")
    print(f"  Authenticated: {connection_test['authenticated']}")
    
    # Show webhook configuration
    def webhook_callback(data):
        print(f"Webhook received: {data}")
    
    webhook_config = client.create_webhook_handler(webhook_callback)
    print(f"\n🪝 Webhook configuration:")
    print(f"  URL: {webhook_config['url']}")
    print(f"  Events: {', '.join(webhook_config['events'][:2])}...")


def main():
    """Run all examples."""
    print("\n")
    print("╔" + "═" * 58 + "╗")
    print("║" + " " * 58 + "║")
    print("║" + "  🔮 EverLight Aetherius Archive - Usage Examples  🔮".center(58) + "║")
    print("║" + " " * 58 + "║")
    print("╚" + "═" * 58 + "╝")
    
    # Run synchronous examples
    example_1_document_processing()
    example_2_mcp_server_setup()
    example_4_nextcloud_client()
    
    # Run async example
    print("\n")
    asyncio.run(example_3_mcp_request_handling())
    
    print("\n\n" + "=" * 60)
    print("✨ All examples completed successfully!")
    print("=" * 60)
    print("\n📖 For more information, see MODEL_DEVELOPMENT.md")
    print("🚀 To start the MCP server: python mcp_server.py")
    print("\n")


if __name__ == "__main__":
    main()

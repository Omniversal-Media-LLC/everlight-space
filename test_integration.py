#!/usr/bin/env python3
"""
test_integration.py

Integration tests for the complete EverLight Aetherius Archive system.
Tests end-to-end workflows including document processing, MCP server, and API integration.
"""

import asyncio
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from everlight_context.models import DocumentProcessor
from everlight_context.mcp import MCPServer
from everlight_context.mcp.handlers import ContextHandler, ToolHandler, ResourceHandler
from everlight_context.api import NextcloudAssistantClient, APIConfig


async def test_complete_workflow():
    """Test complete workflow from document processing to MCP API."""
    print("=" * 70)
    print("🧪 Integration Test: Complete Workflow")
    print("=" * 70)
    print()
    
    # Step 1: Document Processing
    print("Step 1: Document Processing")
    print("-" * 40)
    processor = DocumentProcessor(use_embeddings=True)
    processor.initialize()
    
    test_docs = [
        {
            'filename': 'doc1.txt',
            'content': 'The mystical archive holds ancient knowledge and wisdom.'
        },
        {
            'filename': 'doc2.txt',
            'content': 'A guide to understanding the Aetherius vault systems.'
        }
    ]
    
    results = processor.process_batch(test_docs)
    assert len(results) == 2, "Should process 2 documents"
    print(f"✅ Processed {len(results)} documents")
    
    # Step 2: Semantic Search
    print("\nStep 2: Semantic Search")
    print("-" * 40)
    search_results = processor.search_similar_documents("ancient wisdom", top_k=2)
    assert len(search_results) > 0, "Should find similar documents"
    print(f"✅ Found {len(search_results)} similar documents")
    for result in search_results:
        print(f"   - {result['filename']} (similarity: {result['similarity']:.3f})")
    
    # Step 3: MCP Server Setup
    print("\nStep 3: MCP Server Setup")
    print("-" * 40)
    server = MCPServer(name="test-integration-server", version="1.0.0")
    
    context_handler = ContextHandler("everlight_context/logs/")
    tool_handler = ToolHandler("everlight_context/logs/")
    resource_handler = ResourceHandler("everlight_context/logs/")
    
    server.register_context_handler(context_handler.get_context)
    server.register_tool(
        name="search",
        handler=tool_handler.search_documents,
        description="Search documents",
        parameters={
            "type": "object",
            "properties": {"query": {"type": "string"}},
            "required": ["query"]
        }
    )
    print(f"✅ MCP Server configured with {len(server.tools)} tools")
    
    # Step 4: MCP Request Handling
    print("\nStep 4: MCP Request Handling")
    print("-" * 40)
    
    # Initialize request
    init_req = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "initialize",
        "params": {}
    }
    init_resp = await server.handle_request(init_req)
    assert "result" in init_resp, "Should have result in response"
    print("✅ Initialize request handled")
    
    # List tools request
    list_req = {
        "jsonrpc": "2.0",
        "id": 2,
        "method": "tools/list",
        "params": {}
    }
    list_resp = await server.handle_request(list_req)
    assert len(list_resp["result"]["tools"]) > 0, "Should have tools"
    print(f"✅ Tools list request handled ({len(list_resp['result']['tools'])} tools)")
    
    # Context request
    ctx_req = {
        "jsonrpc": "2.0",
        "id": 3,
        "method": "context/get",
        "params": {}
    }
    ctx_resp = await server.handle_request(ctx_req)
    assert "result" in ctx_resp, "Should have context result"
    print("✅ Context request handled")
    
    # Step 5: API Configuration
    print("\nStep 5: API Configuration")
    print("-" * 40)
    config = APIConfig()
    config.set('test.key', 'test_value')
    assert config.get('test.key') == 'test_value', "Config should store values"
    print("✅ API configuration working")
    
    # Step 6: Nextcloud Client
    print("\nStep 6: Nextcloud Client")
    print("-" * 40)
    client = NextcloudAssistantClient(
        base_url="https://test.example.com",
        username="test",
        app_password="test123"
    )
    
    # Test async methods
    prompt_result = await client.send_prompt("Test prompt")
    assert prompt_result['success'], "Prompt should succeed"
    print("✅ Nextcloud client prompt handling")
    
    register_result = await client.register_provider({
        'name': 'Test Archive',
        'version': '1.0.0'
    })
    assert register_result['success'], "Registration should succeed"
    print("✅ Nextcloud provider registration")
    
    print("\n" + "=" * 70)
    print("✨ Integration Test: ALL PASSED ✨")
    print("=" * 70)
    return True


async def test_mcp_error_handling():
    """Test MCP server error handling."""
    print("\n" + "=" * 70)
    print("🧪 Integration Test: Error Handling")
    print("=" * 70)
    print()
    
    server = MCPServer(name="error-test-server")
    
    # Test invalid method
    invalid_req = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "invalid_method",
        "params": {}
    }
    response = await server.handle_request(invalid_req)
    assert "error" in response, "Should return error for invalid method"
    print("✅ Invalid method error handling")
    
    # Test invalid tool call
    def test_tool(required_param):
        return {"result": "ok"}
    
    server.register_tool(
        name="test_tool",
        handler=test_tool,
        description="Test",
        parameters={"type": "object", "properties": {"required_param": {"type": "string"}}}
    )
    
    invalid_call = {
        "jsonrpc": "2.0",
        "id": 2,
        "method": "tools/call",
        "params": {
            "name": "nonexistent_tool",
            "arguments": {}
        }
    }
    response = await server.handle_request(invalid_call)
    assert "error" in response, "Should return error for nonexistent tool"
    print("✅ Invalid tool call error handling")
    
    print("\n" + "=" * 70)
    print("✨ Error Handling Test: ALL PASSED ✨")
    print("=" * 70)
    return True


async def test_performance():
    """Test performance with multiple documents."""
    print("\n" + "=" * 70)
    print("🧪 Integration Test: Performance")
    print("=" * 70)
    print()
    
    import time
    
    processor = DocumentProcessor(use_embeddings=True)
    processor.initialize()
    
    # Generate test documents
    num_docs = 50
    docs = [
        {
            'filename': f'doc_{i}.txt',
            'content': f'Document {i} content with unique identifier {i*7} and some text.'
        }
        for i in range(num_docs)
    ]
    
    # Measure processing time
    start_time = time.time()
    results = processor.process_batch(docs)
    processing_time = time.time() - start_time
    
    assert len(results) == num_docs, f"Should process {num_docs} documents"
    avg_time = processing_time / num_docs
    print(f"✅ Processed {num_docs} documents in {processing_time:.3f}s")
    print(f"   Average: {avg_time*1000:.2f}ms per document")
    
    # Test search performance
    start_time = time.time()
    search_results = processor.search_similar_documents("unique identifier", top_k=5)
    search_time = time.time() - start_time
    
    assert len(search_results) == 5, "Should return top 5 results"
    print(f"✅ Searched {num_docs} documents in {search_time*1000:.2f}ms")
    
    print("\n" + "=" * 70)
    print("✨ Performance Test: ALL PASSED ✨")
    print("=" * 70)
    return True


async def run_all_integration_tests():
    """Run all integration tests."""
    print("\n")
    print("╔" + "═" * 68 + "╗")
    print("║" + " " * 68 + "║")
    print("║" + "  🔮 EverLight Archive - Integration Tests  🔮".center(68) + "║")
    print("║" + " " * 68 + "║")
    print("╚" + "═" * 68 + "╝")
    print()
    
    try:
        await test_complete_workflow()
        await test_mcp_error_handling()
        await test_performance()
        
        print("\n")
        print("╔" + "═" * 68 + "╗")
        print("║" + " " * 68 + "║")
        print("║" + "  ✨ ALL INTEGRATION TESTS PASSED ✨".center(68) + "║")
        print("║" + " " * 68 + "║")
        print("╚" + "═" * 68 + "╝")
        print()
        return True
        
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
        return False
    except Exception as e:
        print(f"\n❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = asyncio.run(run_all_integration_tests())
    sys.exit(0 if success else 1)

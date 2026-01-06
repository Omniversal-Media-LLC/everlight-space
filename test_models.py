"""
test_models.py

Basic tests for model development infrastructure.
Validates that core components are working correctly.
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from everlight_context.models import BaseAetheriusModel, EmbeddingModel, DocumentProcessor


def test_base_model():
    """Test base model functionality."""
    print("🧪 Testing BaseAetheriusModel...")
    
    class TestModel(BaseAetheriusModel):
        def initialize(self):
            self._initialized = True
            return True
        
        def process(self, input_data):
            return {"processed": input_data}
    
    model = TestModel("test-model")
    assert model.model_name == "test-model"
    assert not model.is_initialized()
    
    result = model.initialize()
    assert result is True
    assert model.is_initialized()
    
    output = model.process("test input")
    assert output["processed"] == "test input"
    
    print("✅ BaseAetheriusModel tests passed")


def test_embedding_model():
    """Test embedding model."""
    print("🧪 Testing EmbeddingModel...")
    
    model = EmbeddingModel()
    model.initialize()
    
    # Test single text
    embedding = model.process("test text")
    assert embedding.shape[0] == 1
    assert embedding.shape[1] == 384  # default embedding dim
    
    # Test multiple texts
    embeddings = model.process(["text 1", "text 2", "text 3"])
    assert embeddings.shape[0] == 3
    assert embeddings.shape[1] == 384
    
    # Test similarity computation
    emb1 = model.process("cat")[0]
    emb2 = model.process("cat")[0]
    similarity = model.compute_similarity(emb1, emb2)
    assert similarity > 0.99  # Same text should have high similarity
    
    print("✅ EmbeddingModel tests passed")


def test_document_processor():
    """Test document processor."""
    print("🧪 Testing DocumentProcessor...")
    
    processor = DocumentProcessor()
    processor.initialize()
    
    # Test document processing
    doc = {
        'filename': 'test.txt',
        'content': 'This is a test document for the EverLight Aetherius Archive. It contains mystical knowledge.',
        'metadata': {'author': 'Tester'}
    }
    
    result = processor.process(doc)
    
    assert result['filename'] == 'test.txt'
    assert 'summary' in result
    assert result['word_count'] > 0
    assert result['char_count'] > 0
    assert 'embedding' in result  # Should have embedding by default
    
    # Test cached retrieval
    cached = processor.get_cached_document('test.txt')
    assert cached is not None
    assert cached['filename'] == 'test.txt'
    
    # Test batch processing
    docs = [doc, {'filename': 'test2.txt', 'content': 'Another test document.'}]
    results = processor.process_batch(docs)
    assert len(results) == 2
    
    # Test search
    search_results = processor.search_similar_documents("mystical archive", top_k=2)
    assert len(search_results) <= 2
    
    print("✅ DocumentProcessor tests passed")


def test_mcp_server():
    """Test MCP server setup."""
    print("🧪 Testing MCP Server...")
    
    from everlight_context.mcp import MCPServer
    from everlight_context.mcp.handlers import ContextHandler, ToolHandler, ResourceHandler
    
    server = MCPServer(name="test-server", version="1.0.0")
    
    # Register a test tool
    def test_tool(arg1):
        return {"result": f"Tool executed with {arg1}"}
    
    server.register_tool(
        name="test_tool",
        handler=test_tool,
        description="Test tool",
        parameters={"type": "object", "properties": {"arg1": {"type": "string"}}}
    )
    
    assert "test_tool" in server.tools
    
    # Register a test resource
    def test_resource():
        return "Test resource content"
    
    server.register_resource(
        uri="test://resource",
        handler=test_resource,
        name="Test Resource",
        description="A test resource"
    )
    
    assert "test://resource" in server.resources
    
    print("✅ MCP Server tests passed")


def test_api_config():
    """Test API configuration."""
    print("🧪 Testing API Configuration...")
    
    from everlight_context.api import APIConfig
    
    config = APIConfig()
    
    # Test default configuration
    assert config.get('mcp.host') is not None
    assert config.get('mcp.port') is not None
    
    # Test set/get
    config.set('test.key', 'test_value')
    assert config.get('test.key') == 'test_value'
    
    # Test nested keys
    config.set('nested.deep.key', 42)
    assert config.get('nested.deep.key') == 42
    
    print("✅ API Configuration tests passed")


def run_all_tests():
    """Run all tests."""
    print("=" * 60)
    print("🔮 EverLight Aetherius Archive - Model Tests")
    print("=" * 60)
    print()
    
    try:
        test_base_model()
        print()
        test_embedding_model()
        print()
        test_document_processor()
        print()
        test_mcp_server()
        print()
        test_api_config()
        print()
        print("=" * 60)
        print("✨ All tests passed! The Archive is operational. ✨")
        print("=" * 60)
        return True
    except AssertionError as e:
        print(f"❌ Test failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)

# Model Development Guide

## EverLight Aetherius Archive - Model Development Infrastructure

This guide covers the model development infrastructure built into the EverLight Aetherius Archive for eventual API/MCP connection with Nextcloud Assistant.

## Architecture Overview

The model development infrastructure consists of three main components:

### 1. Models Module (`everlight_context/models/`)

Contains the core model classes for document processing and semantic understanding:

- **BaseAetheriusModel**: Abstract base class for all models
- **EmbeddingModel**: Transforms text into vector embeddings for semantic search
- **DocumentProcessor**: Processes documents for analysis, summarization, and retrieval

### 2. MCP Server (`everlight_context/mcp/`)

Implements the Model Context Protocol for standardized AI assistant integration:

- **MCPServer**: Core server implementing MCP specification
- **ContextHandler**: Manages archive context and metadata
- **ToolHandler**: Exposes document processing tools
- **ResourceHandler**: Provides access to archive resources

### 3. API Integration (`everlight_context/api/`)

Handles external service integrations, specifically Nextcloud Assistant:

- **NextcloudAssistantClient**: Client for Nextcloud Assistant API
- **APIConfig**: Configuration management for API connections

## Quick Start

### Basic Usage

1. **Process Documents with Models**

```python
from everlight_context.models import DocumentProcessor

# Initialize processor
processor = DocumentProcessor(use_embeddings=True)
processor.initialize()

# Process a document
result = processor.process({
    'filename': 'example.txt',
    'content': 'Your document content here...'
})

print(f"Summary: {result['summary']}")
print(f"Word count: {result['word_count']}")
```

2. **Start MCP Server**

```bash
# Using command line
python mcp_server.py --host 0.0.0.0 --port 8080 --logs-dir everlight_context/logs/

# Or with configuration file
python mcp_server.py --config config.json
```

3. **Connect to Nextcloud Assistant**

```python
from everlight_context.api import NextcloudAssistantClient

# Initialize client
client = NextcloudAssistantClient(
    base_url='https://your-nextcloud.com',
    username='your-username',
    app_password='your-app-password'
)

# Test connection
result = client.test_connection()
print(result)
```

## Model Development Workflow

### 1. Document Processing Pipeline

The document processor provides a complete pipeline for analyzing archive documents:

```python
from everlight_context.models import DocumentProcessor

processor = DocumentProcessor()
processor.initialize()

# Process single document
doc_data = {
    'filename': 'archive_entry.md',
    'content': 'The dawn of Aetherius begins...',
    'metadata': {'author': 'Archivist', 'date': '2026-01-04'}
}

result = processor.process(doc_data)

# Process batch of documents
documents = [doc_data, ...]
results = processor.process_batch(documents)
```

### 2. Semantic Search

Use embeddings to find similar documents:

```python
# Search for documents similar to a query
results = processor.search_similar_documents(
    query_text="mystical vault of knowledge",
    top_k=5
)

for doc in results:
    print(f"{doc['filename']}: {doc['similarity']:.3f}")
```

### 3. Custom Model Development

Extend the base model class for custom implementations:

```python
from everlight_context.models import BaseAetheriusModel

class CustomModel(BaseAetheriusModel):
    def __init__(self, model_name="custom-model"):
        super().__init__(model_name)
    
    def initialize(self):
        # Load your model
        self._initialized = True
        return True
    
    def process(self, input_data):
        # Your processing logic
        return {"result": "processed"}
```

## MCP Server Integration

### Available Tools

The MCP server exposes these tools to AI assistants:

1. **list_documents**: List all documents in the archive
2. **get_document**: Retrieve a specific document
3. **search_documents**: Search for similar documents
4. **summarize_document**: Generate document summary

### Available Resources

- `archive://index`: Complete archive index
- `archive://documents/{filename}`: Individual document content

### Example MCP Request

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "search_documents",
    "arguments": {
      "query": "mystical knowledge",
      "top_k": 3
    }
  }
}
```

## Nextcloud Assistant Integration

### Configuration

Create a `config.json` file:

```json
{
  "nextcloud": {
    "url": "https://your-nextcloud.com",
    "username": "your-username",
    "app_password": "your-app-password"
  },
  "mcp": {
    "host": "0.0.0.0",
    "port": 8080
  }
}
```

Or use environment variables (see `.env.example`).

### Registering as a Provider

```python
from everlight_context.api import NextcloudAssistantClient

client = NextcloudAssistantClient(
    base_url=config['nextcloud']['url'],
    username=config['nextcloud']['username'],
    app_password=config['nextcloud']['app_password']
)

# Register the archive as a context provider
response = await client.register_provider({
    'name': 'EverLight Aetherius Archive',
    'version': '1.0.0',
    'capabilities': ['document_search', 'semantic_retrieval', 'summarization']
})
```

## Advanced Features

### Embedding Model Customization

Replace placeholder embeddings with production models:

```python
# In embeddings.py, modify initialize() method:
from sentence_transformers import SentenceTransformer

def initialize(self):
    self._model = SentenceTransformer('all-MiniLM-L6-v2')
    self._initialized = True
    return True

def process(self, input_data):
    if isinstance(input_data, str):
        input_data = [input_data]
    return self._model.encode(input_data)
```

### Custom Tool Registration

Add custom tools to the MCP server:

```python
def custom_tool(**kwargs):
    # Your tool logic
    return {"result": "custom output"}

server.register_tool(
    name="custom_tool",
    handler=custom_tool,
    description="Description of custom tool",
    parameters={
        "type": "object",
        "properties": {
            "param": {"type": "string"}
        },
        "required": ["param"]
    }
)
```

## Testing

### Test Document Processing

```python
from everlight_context.models import DocumentProcessor

processor = DocumentProcessor()
processor.initialize()

test_doc = {
    'filename': 'test.txt',
    'content': 'Test content for the Archive'
}

result = processor.process(test_doc)
assert 'summary' in result
assert result['word_count'] > 0
```

### Test MCP Server

```bash
# Start server
python mcp_server.py --port 8080

# In another terminal, test with curl or MCP client
curl -X POST http://localhost:8080 \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list"}'
```

## Future Enhancements

- [ ] Production embedding models (sentence-transformers, OpenAI)
- [ ] HTTP/WebSocket transport for MCP server
- [ ] Advanced document chunking and retrieval
- [ ] Fine-tuning support for custom models
- [ ] Multi-modal support (images, PDFs)
- [ ] Real-time indexing and updates
- [ ] Authentication and authorization
- [ ] Metrics and monitoring

## Troubleshooting

### Issue: Models not initializing
- Check that numpy is installed: `pip install numpy`
- Verify file paths are correct

### Issue: MCP server not accessible
- Check firewall settings
- Verify port is not already in use: `netstat -an | grep 8080`

### Issue: Nextcloud connection fails
- Verify Nextcloud URL is correct
- Check app password is valid
- Ensure network connectivity

## Support

For issues or questions about model development:
1. Check existing documentation
2. Review code comments and docstrings
3. Examine example configurations

---

**May your models bring clarity to the Archive's mysteries.**

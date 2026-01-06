#!/usr/bin/env python3
"""
quick_start.py

Quick start script for the EverLight Aetherius Archive.
Demonstrates core functionality in a simple, interactive way.
"""

import sys
from everlight_context.models import DocumentProcessor
from everlight_context.loader import load_documents


def main():
    print("=" * 70)
    print("🔮 EverLight Aetherius Archive - Quick Start 🔮".center(70))
    print("=" * 70)
    print()
    
    # Initialize document processor
    print("📚 Initializing Document Processor...")
    processor = DocumentProcessor(use_embeddings=True)
    processor.initialize()
    print("✅ Processor ready!\n")
    
    # Load documents from logs directory
    logs_dir = "everlight_context/logs/"
    print(f"📂 Loading documents from {logs_dir}...")
    docs = load_documents(logs_dir)
    
    if not docs:
        print("⚠️  No documents found in the archive.")
        print(f"   Add .html, .md, or .txt files to {logs_dir} to get started.")
        return
    
    print(f"✅ Found {len(docs)} document(s)\n")
    
    # Process each document
    print("📊 Processing documents...\n")
    for filename, content in docs:
        result = processor.process({
            'filename': filename,
            'content': content
        })
        
        print(f"  📄 {filename}")
        print(f"     Words: {result['word_count']} | Chars: {result['char_count']}")
        print(f"     Summary: {result['summary'][:100]}...")
        print()
    
    # Demonstrate semantic search
    print("=" * 70)
    print("🔍 Semantic Search Demonstration")
    print("=" * 70)
    print()
    
    queries = [
        "archive knowledge",
        "mystical vault",
        "historical records"
    ]
    
    for query in queries:
        print(f"Query: '{query}'")
        results = processor.search_similar_documents(query, top_k=min(2, len(docs)))
        
        if results:
            for i, result in enumerate(results, 1):
                print(f"  {i}. {result['filename']} (similarity: {result['similarity']:.3f})")
        else:
            print("  No results found")
        print()
    
    # Show next steps
    print("=" * 70)
    print("✨ Next Steps")
    print("=" * 70)
    print()
    print("1. 🚀 Start MCP Server:")
    print("   python mcp_server.py --port 8080")
    print()
    print("2. 📖 Read the Documentation:")
    print("   cat MODEL_DEVELOPMENT.md")
    print()
    print("3. 🧪 Run Tests:")
    print("   python test_models.py")
    print()
    print("4. 📝 See More Examples:")
    print("   python example_usage.py")
    print()
    print("5. 🔧 Configure Nextcloud:")
    print("   cp config.example.json config.json")
    print("   # Edit config.json with your Nextcloud details")
    print()
    print("=" * 70)
    print("🌟 The Archive awaits your exploration! 🌟".center(70))
    print("=" * 70)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Farewell, Archivist!")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

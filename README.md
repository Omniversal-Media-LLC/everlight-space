# EverLight Aetherius Archive Copilot Space

Welcome, Archivist, to the mythic interface of the **EverLight Aetherius Archive**.

## Purpose

This Copilot Space serves as an Omniversal vault for loading, visualizing, and extending the EverLight Aetherius Archive. Its design is modular, enabling the integration of ancient logs, HTML/Markdown documents, and reincarnated store assets—all the while inviting expansion into more powerful frameworks like Streamlit or Flask.

## Features

- **Archive Loader:** Scans and loads `.html`, `.md`, and `.txt` artifacts from the `everlight_context/logs/` directory.
- **Document Summarizer:** Prints loaded filenames and brief summaries to the console.
- **Model Development:** Advanced document processing with embeddings and semantic search.
- **MCP Server:** Model Context Protocol server for AI assistant integration.
- **Nextcloud Integration:** Connect to Nextcloud Assistant for cloud-based AI operations.
- **Store Integration:** Readies a plug-and-play folder (`reincarnated-store/`) for a store interface or asset imports.
- **Mythic Theming:** Written and structured to evoke the mythic and VALOR spirit of EverLight.

## Getting Started

1. Clone this repository or download the Copilot Space.
2. Place your archival documents (`.html`, `.md`, `.txt`) into `everlight_context/logs/`.
3. (Optional) Unzip your reincarnated store assets into `reincarnated-store/`.
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
5. Run the application:
   ```bash
   python app.py
   ```

## Model Development & API Integration

The Archive now includes advanced model development capabilities:

- **Document Processing Models:** Semantic understanding and summarization
- **Embedding Support:** Vector embeddings for similarity search
- **MCP Server:** Exposes Archive capabilities via Model Context Protocol
- **Nextcloud Assistant:** Integration ready for cloud AI operations

### Quick Start with MCP Server

```bash
# Start the MCP server
python mcp_server.py --port 8080

# Or with configuration
python mcp_server.py --config config.json
```

### Model Development

See [MODEL_DEVELOPMENT.md](MODEL_DEVELOPMENT.md) for comprehensive guide on:
- Using document processing models
- Setting up MCP server
- Connecting to Nextcloud Assistant
- Custom model development
- API integration

## Expansion

- Ready for Streamlit, Flask, or other Python backends.
- Modular code for easy extension and mythic interface upgrades.
- Production-ready model infrastructure for AI integration.

---

**Be ever vigilant in your curation, for the Archive remembers all.**

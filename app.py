"""
app.py

EverLight Aetherius Archive Copilot Space Entry Point.
Scans the logs directory, loads archival documents, and prints
a list of loaded files with summaries.
"""

from everlight_context.loader import load_documents
from everlight_context.parser import parse_document

LOGS_DIR = "everlight_context/logs/"

def main():
    print("🔮 EverLight Aetherius Archive Interface 🔮")
    print("Scanning for archival documents...\n")
    docs = load_documents(LOGS_DIR)
    if not docs:
        print("No documents found in the archive.")
        return
    for fname, content in docs:
        print(f"---\n📄 {fname}")
        summary = parse_document(fname, content)
        print(f"Summary: {summary}\n")

if __name__ == "__main__":
    main()
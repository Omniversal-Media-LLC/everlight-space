"""
loader.py

Scans the logs directory for HTML, Markdown, and plain-text log files.
Loads and returns their contents for further processing or visualization.
"""

import os

SUPPORTED_EXTENSIONS = ('.html', '.md', '.txt')

def scan_logs_dir(logs_dir):
    """
    Scans the provided directory for supported archive files.
    Returns a list of file paths.
    """
    if not os.path.exists(logs_dir):
        return []
    files = []
    for fname in os.listdir(logs_dir):
        if fname.lower().endswith(SUPPORTED_EXTENSIONS):
            files.append(os.path.join(logs_dir, fname))
    return files

def load_documents(logs_dir):
    """
    Loads all supported documents from the given logs directory.
    Returns a list of tuples: (filename, content).
    """
    files = scan_logs_dir(logs_dir)
    docs = []
    for path in files:
        try:
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            docs.append((os.path.basename(path), content))
        except Exception as e:
            docs.append((os.path.basename(path), f"[ERROR LOADING FILE: {e}]"))
    return docs
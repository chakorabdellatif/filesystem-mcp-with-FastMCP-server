"""
Configuration for MCP Filesystem Server
"""

import os
from pathlib import Path

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# Server configuration
MCP_SERVER_HOST = os.getenv("MCP_SERVER_HOST", "127.0.0.1")
MCP_SERVER_PORT = int(os.getenv("MCP_SERVER_PORT", "8000"))

# Get the project root directory (parent of server/)
PROJECT_ROOT = Path(__file__).parent.parent

# Workspace directory - always inside the project
WORKSPACE_DIR = PROJECT_ROOT / "workspace"

# Ensure workspace exists
WORKSPACE_DIR.mkdir(exist_ok=True)

# OpenAI configuration (for host)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Allowed file extensions for safety
ALLOWED_EXTENSIONS = {
    ".txt",
    ".md",
    ".json",
    ".csv",
    ".xml",
    ".yaml",
    ".yml",
    ".py",
    ".js",
    ".html",
    ".css",
    ".pdf",
    ".log",
}

# Maximum file size (10MB)
MAX_FILE_SIZE = 10 * 1024 * 1024

import sys
sys.stderr.write(f"📁 Workspace directory: {WORKSPACE_DIR}\n")

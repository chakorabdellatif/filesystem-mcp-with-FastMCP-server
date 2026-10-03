"""
Streamlit Cloud Entrypoint for MCP Filesystem Assistant
ENIAD Multi-Agent Systems & Tool Integration
"""

import sys
from pathlib import Path

# Ensure root directory is on python path
ROOT_DIR = Path(__file__).parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

# Run the host app
import host.app

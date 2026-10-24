"""
LiteLLM Universal Multi-Model Proxy Launcher
Routes calls across local Ollama, Gemini, OpenAI, and Anthropic
with automatic fallback and cost tracking.
"""

import os
import subprocess
import sys
from pathlib import Path


def run_litellm():
    config_path = Path(__file__).parent / "litellm_config.yaml"
    port = os.environ.get("LITELLM_PORT", "4000")

    print("==================================================")
    print("  🚀 Starting LiteLLM Multi-Provider Proxy")
    print(f"  📄 Config: {config_path}")
    print(f"  🔗 Listening on: http://localhost:{port}")
    print("==================================================")

    cmd = [
        sys.executable,
        "-m",
        "litellm",
        "--config",
        str(config_path),
        "--port",
        str(port),
    ]

    try:
        subprocess.run(cmd, check=True)
    except FileNotFoundError:
        print("ℹ️ LiteLLM package not installed in current Python env.")
        print("💡 Install with: `pip install litellm[proxy]`")
    except KeyboardInterrupt:
        print("\nStopping LiteLLM Proxy...")


if __name__ == "__main__":
    run_litellm()

"""
Graphify CLI Tool
Scan any repository or codebase to generate AST knowledge graphs and Mermaid diagrams.
Usage:
  python run_graphify.py [path_to_repo] [--mermaid] [--json]
"""

import argparse
import sys
from pathlib import Path

# Add tools parent to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from tools.graphify_engine import GraphifyEngine


def main():
    parser = argparse.ArgumentParser(description="Graphify AST Codebase Knowledge Graph Generator")
    parser.add_argument("path", nargs="?", default=".", help="Path to repository to scan (default: current directory)")
    parser.add_argument("--mermaid", action="store_true", help="Output Mermaid class diagram")
    parser.add_argument("--json", action="store_true", help="Output raw JSON graph data")
    parser.add_argument("--output", "-o", help="Optional output file path to save result")

    args = parser.parse_args()
    target_path = Path(args.path).resolve()

    print(f"🔍 Scanning codebase at: {target_path}")
    engine = GraphifyEngine(str(target_path))
    result = engine.scan_repository()

    print("==================================================")
    print(f"  📁 Files Scanned: {result['files_scanned']}")
    print(f"  🏷️ Symbols Extracted: {result['symbols_extracted']}")
    print(f"  📍 Graph Nodes: {result['nodes_count']}")
    print(f"  🔗 Dependency Edges: {result['edges_count']}")
    print("==================================================\n")

    if args.mermaid:
        output_content = engine.generate_mermaid_diagram()
    elif args.json:
        import json
        output_content = json.dumps(result, indent=2)
    else:
        output_content = engine.generate_mermaid_diagram(max_nodes=20)

    if args.output:
        out_file = Path(args.output).resolve()
        out_file.parent.mkdir(parents=True, exist_ok=True)
        with open(out_file, "w", encoding="utf-8") as f:
            f.write(output_content)
        print(f"✅ Output saved to: {out_file}")
    else:
        print(output_content)


if __name__ == "__main__":
    main()

"""
Graphify AST Codebase Knowledge Graph Engine
Inspired by Graphify-Labs/graphify
Deterministic AST-level static analysis and knowledge graph generation
for Python, JavaScript, TypeScript, and SQL codebases.
"""

import ast
import json
import os
import re
from pathlib import Path
from typing import Any, Dict, List, Set


class GraphifyEngine:
    def __init__(self, root_dir: str):
        self.root_dir = Path(root_dir)
        self.nodes: List[Dict[str, Any]] = []
        self.edges: List[Dict[str, Any]] = []
        self.file_count = 0
        self.symbol_count = 0

    def analyze_python_file(self, file_path: Path):
        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()

            rel_path = file_path.relative_to(self.root_dir).as_posix()
            tree = ast.parse(content, filename=str(file_path))

            file_node_id = f"file::{rel_path}"
            self.nodes.append({"id": file_node_id, "type": "file", "name": file_path.name, "path": rel_path})

            for node in ast.iter_child_nodes(tree):
                if isinstance(node, ast.ClassDef):
                    class_id = f"class::{rel_path}::{node.name}"
                    bases = [b.id for b in node.bases if isinstance(b, ast.Name)]
                    self.nodes.append(
                        {
                            "id": class_id,
                            "type": "class",
                            "name": node.name,
                            "file": rel_path,
                            "bases": bases,
                            "methods": [m.name for m in node.body if isinstance(m, (ast.FunctionDef, ast.AsyncFunctionDef))],
                        }
                    )
                    self.edges.append({"source": file_node_id, "target": class_id, "relation": "defines"})
                    self.symbol_count += 1

                elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    fn_id = f"fn::{rel_path}::{node.name}"
                    self.nodes.append(
                        {
                            "id": fn_id,
                            "type": "function",
                            "name": node.name,
                            "file": rel_path,
                            "is_async": isinstance(node, ast.AsyncFunctionDef),
                        }
                    )
                    self.edges.append({"source": file_node_id, "target": fn_id, "relation": "defines"})
                    self.symbol_count += 1

                elif isinstance(node, ast.Import):
                    for alias in node.names:
                        self.edges.append({"source": file_node_id, "target": f"module::{alias.name}", "relation": "imports"})

                elif isinstance(node, ast.ImportFrom):
                    mod = node.module or ""
                    self.edges.append({"source": file_node_id, "target": f"module::{mod}", "relation": "imports_from"})

        except Exception:
            pass

    def scan_repository(self) -> Dict[str, Any]:
        ignore_dirs = {".git", ".venv", "node_modules", "__pycache__", ".ruff_cache", ".pytest_cache", "dist", "build"}

        for root, dirs, files in os.walk(self.root_dir):
            dirs[:] = [d for d in dirs if d not in ignore_dirs]
            for file in files:
                fpath = Path(root) / file
                if file.endswith(".py"):
                    self.file_count += 1
                    self.analyze_python_file(fpath)
                elif file.endswith((".js", ".ts", ".jsx", ".tsx")):
                    self.file_count += 1
                    rel_path = fpath.relative_to(self.root_dir).as_posix()
                    self.nodes.append({"id": f"file::{rel_path}", "type": "script", "name": file, "path": rel_path})

        return {
            "root": str(self.root_dir),
            "files_scanned": self.file_count,
            "symbols_extracted": self.symbol_count,
            "nodes_count": len(self.nodes),
            "edges_count": len(self.edges),
            "nodes": self.nodes,
            "edges": self.edges,
        }

    def generate_mermaid_diagram(self, max_nodes: int = 30) -> str:
        lines = ["```mermaid", "classDiagram"]
        class_nodes = [n for n in self.nodes if n.get("type") == "class"][:max_nodes]

        for cn in class_nodes:
            name = cn["name"]
            lines.append(f"    class {name} {{")
            for m in cn.get("methods", [])[:5]:
                lines.append(f"        +{m}()")
            lines.append("    }")
            for base in cn.get("bases", []):
                lines.append(f"    {base} <|-- {name}")

        lines.append("```")
        return "\n".join(lines)


def build_graph_for_path(path: str) -> Dict[str, Any]:
    engine = GraphifyEngine(path)
    return engine.scan_repository()

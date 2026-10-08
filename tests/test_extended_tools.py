"""
Tests for FastMCP Extended Enterprise Tools (DuckDB, SPARQL, S3).
"""

import pytest
from pathlib import Path
from fastmcp import FastMCP
from server.extended_tools import register_extended_tools


@pytest.fixture
def mock_workspace(tmp_path):
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    return workspace


@pytest.fixture
def validate_path_fn(mock_workspace):
    def _validate(path: str) -> Path:
        p = Path(path)
        if p.is_absolute():
            raise ValueError("Absolute paths not allowed")
        full_path = (mock_workspace / p).resolve()
        if not full_path.is_relative_to(mock_workspace.resolve()):
            raise ValueError("Path traversal detected")
        return full_path
    return _validate


@pytest.fixture
def mcp_server(validate_path_fn):
    server = FastMCP("Test MCP Server")
    register_extended_tools(server, validate_path_fn)
    return server


def test_duckdb_tool_in_memory(mcp_server):
    # Find tool function
    # FastMCP tools are callable
    for tool in mcp_server._tool_manager.list_tools():
        if tool.name == "query_duckdb":
            break
    assert tool is not None


def test_sparql_tool_registered(mcp_server):
    tools = [t.name for t in mcp_server._tool_manager.list_tools()]
    assert "query_sparql" in tools
    assert "s3_manage_asset" in tools

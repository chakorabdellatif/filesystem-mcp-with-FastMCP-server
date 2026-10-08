"""
Extended Multi-Tool Capabilities for FastMCP Server
Provides DuckDB OLAP, RDFLib SPARQL Knowledge Graph, and S3 Asset Operations.
"""

import json
from pathlib import Path
from typing import Any, Dict, Optional

try:
    import duckdb
except ImportError:
    duckdb = None

try:
    import rdflib
except ImportError:
    rdflib = None

try:
    import boto3
    from botocore.exceptions import BotoCoreError, ClientError
except ImportError:
    boto3 = None
    BotoCoreError = ClientError = Exception


def register_extended_tools(mcp, validate_path_fn):
    """
    Registers extended enterprise tools on the provided FastMCP server instance.
    """

    # ==================== EXTENDED TOOL 1: DUCKDB ANALYTICS ====================

    @mcp.tool()
    def query_duckdb(sql_query: str, db_path: Optional[str] = None) -> str:
        """
        Execute high-performance analytical SQL queries on local files (CSV, Parquet, JSON)
        or a persistent DuckDB database file within the workspace.

        Args:
            sql_query: SQL query string (e.g. "SELECT * FROM read_csv_auto('data.csv') LIMIT 10")
            db_path: Optional relative path to a .duckdb file. If omitted, runs in in-memory mode.

        Returns:
            Query results as a formatted markdown table or error message.
        """
        if duckdb is None:
            return "❌ Error: 'duckdb' package is not installed. Install with `pip install duckdb`."

        try:
            if db_path:
                resolved_db = str(validate_path_fn(db_path))
                con = duckdb.connect(resolved_db)
            else:
                con = duckdb.connect(":memory:")

            df = con.execute(sql_query).fetchdf()
            con.close()

            if df.empty:
                return "✅ Query executed successfully. Result set is empty (0 rows)."

            return f"✅ DuckDB Query Results ({len(df)} rows):\n\n{df.to_markdown(index=False)}"
        except Exception as e:
            return f"❌ DuckDB Execution Error: {e!s}"

    # ==================== EXTENDED TOOL 2: SPARQL / KNOWLEDGE GRAPH ====================

    @mcp.tool()
    def query_sparql(sparql_query: str, rdf_file_path: Optional[str] = None, endpoint_url: Optional[str] = None) -> str:
        """
        Execute SPARQL queries over local RDF/OWL ontology files (Turtle .ttl, RDF/XML, JSON-LD)
        or against a remote SPARQL endpoint (e.g. DBpedia, Wikidata).

        Args:
            sparql_query: SPARQL query string (e.g. "SELECT ?s ?p ?o WHERE { ?s ?p ?o } LIMIT 10")
            rdf_file_path: Relative path to local ontology file within workspace.
            endpoint_url: Optional remote SPARQL endpoint URL.

        Returns:
            JSON or formatted string of query bindings.
        """
        if rdflib is None:
            return "❌ Error: 'rdflib' package is not installed. Install with `pip install rdflib`."

        try:
            g = rdflib.Graph()
            if rdf_file_path:
                resolved_rdf = validate_path_fn(rdf_file_path)
                if not resolved_rdf.exists():
                    return f"❌ Error: RDF file '{rdf_file_path}' does not exist."
                g.parse(str(resolved_rdf))
            elif endpoint_url:
                # Query remote SPARQL endpoint
                from rdflib.plugins.sparql.sparql import SPARQLError
                # Simple binding query over endpoint
                g = rdflib.ConjunctiveGraph("SPARQLStore")
                g.open(endpoint_url)
            else:
                return "❌ Error: Provide either 'rdf_file_path' or 'endpoint_url'."

            results = g.query(sparql_query)
            bindings = []
            for row in results:
                row_dict = {}
                for var in results.vars:
                    val = row[var]
                    row_dict[str(var)] = str(val) if val is not None else None
                bindings.append(row_dict)

            if not bindings:
                return "✅ SPARQL query executed successfully. No matching triples found (0 results)."

            return f"✅ SPARQL Results ({len(bindings)} matches):\n```json\n{json.dumps(bindings, indent=2)}\n```"
        except Exception as e:
            return f"❌ SPARQL Execution Error: {e!s}"

    # ==================== EXTENDED TOOL 3: S3 ASSET MANAGEMENT ====================

    @mcp.tool()
    def s3_manage_asset(action: str, bucket_name: str, object_key: str, local_file_path: Optional[str] = None, expiration_seconds: int = 3600) -> str:
        """
        Manage cloud assets in AWS S3 or S3-compatible object stores (listing, uploading, presigned URL generation).

        Args:
            action: One of 'generate_presigned_url', 'upload_file', 'check_exists'
            bucket_name: Name of the S3 bucket
            object_key: Path/key of the object in S3
            local_file_path: Local file path in workspace for uploads
            expiration_seconds: Expiration time in seconds for presigned URLs (default 3600)

        Returns:
            Operation outcome or presigned URL.
        """
        if boto3 is None:
            return "❌ Error: 'boto3' is not installed. Install with `pip install boto3`."

        try:
            s3_client = boto3.client("s3")

            if action == "generate_presigned_url":
                url = s3_client.generate_presigned_url(
                    "get_object",
                    Params={"Bucket": bucket_name, "Key": object_key},
                    ExpiresIn=expiration_seconds,
                )
                return f"✅ Presigned URL generated (expires in {expiration_seconds}s):\n{url}"

            elif action == "upload_file":
                if not local_file_path:
                    return "❌ Error: 'local_file_path' is required for upload."
                resolved_local = validate_path_fn(local_file_path)
                if not resolved_local.exists():
                    return f"❌ Error: Local file '{local_file_path}' does not exist."

                s3_client.upload_file(str(resolved_local), bucket_name, object_key)
                return f"✅ File '{local_file_path}' successfully uploaded to 's3://{bucket_name}/{object_key}'"

            elif action == "check_exists":
                s3_client.head_object(Bucket=bucket_name, Key=object_key)
                return f"✅ Asset exists: 's3://{bucket_name}/{object_key}'"

            else:
                return f"❌ Unsupported action: '{action}'. Choose from 'generate_presigned_url', 'upload_file', 'check_exists'."

        except ClientError as e:
            error_code = e.response.get("Error", {}).get("Code")
            if error_code == "404" and action == "check_exists":
                return f"ℹ️ Asset 's3://{bucket_name}/{object_key}' does not exist."
            return f"❌ S3 ClientError: {e!s}"
        except Exception as e:
            return f"❌ S3 Operation Error: {e!s}"

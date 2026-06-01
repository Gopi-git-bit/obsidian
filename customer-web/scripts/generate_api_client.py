from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BACKEND = ROOT / "backend"
OUT = Path(__file__).resolve().parents[1] / "src" / "api"

sys.path.insert(0, str(BACKEND))

from app.main import app  # noqa: E402


METHOD_NAMES = {
    ("post", "/api/v1/auth/dev-login"): "devLogin",
    ("post", "/api/v1/orders"): "createOrder",
    ("get", "/api/v1/orders"): "listOrders",
    ("get", "/api/v1/orders/{order_id}"): "getOrder",
    ("get", "/api/v1/orders/{order_id}/customer-flow-summary"): "getCustomerFlowSummary",
    ("post", "/api/v1/orders/{order_id}/quote"): "createQuote",
    ("post", "/api/v1/orders/{order_id}/payments/advance"): "recordAdvancePayment",
}


def type_name(name: str) -> str:
    cleaned = re.sub(r"[^a-zA-Z0-9_]", "_", name)
    return cleaned[:1].upper() + cleaned[1:]


def schema_to_ts(schema: dict) -> str:
    schema_type = schema.get("type")
    if "$ref" in schema:
        return type_name(schema["$ref"].rsplit("/", 1)[-1])
    if schema_type == "string":
        return "string"
    if schema_type in {"integer", "number"}:
        return "number"
    if schema_type == "boolean":
        return "boolean"
    if schema_type == "array":
        return f"Array<{schema_to_ts(schema.get('items', {}))}>"
    if schema_type == "object":
        return "Record<string, unknown>"
    if "anyOf" in schema:
        return " | ".join(schema_to_ts(item) for item in schema["anyOf"])
    return "unknown"


def build_types(openapi: dict) -> str:
    lines = ["// Generated from FastAPI OpenAPI. Do not edit by hand.", ""]
    schemas = openapi.get("components", {}).get("schemas", {})
    for name, schema in sorted(schemas.items()):
        if schema.get("type") != "object":
            continue
        required = set(schema.get("required", []))
        lines.append(f"export interface {type_name(name)} {{")
        for prop, prop_schema in schema.get("properties", {}).items():
            optional = "" if prop in required else "?"
            lines.append(f"  {prop}{optional}: {schema_to_ts(prop_schema)};")
        lines.append("}")
        lines.append("")
    return "\n".join(lines)


def build_client(openapi: dict) -> str:
    methods = []
    for (verb, path), method_name in METHOD_NAMES.items():
        if path not in openapi["paths"] or verb not in openapi["paths"][path]:
            raise RuntimeError(f"OpenAPI path missing for generated client: {verb.upper()} {path}")
        params = sorted(set(re.findall(r"{([^}]+)}", path)))
        args = [param for param in params]
        body_arg = "body" if verb != "get" else None
        if body_arg:
            args.append(body_arg)
        args.append("query = {}")
        arg_list = ", ".join(args)
        template_path = re.sub(r"{([^}]+)}", r"${\1}", path)
        body_line = ", body: JSON.stringify(body)" if body_arg else ""
        methods.append(
            f"""  async {method_name}({arg_list}) {{
    return request(this.baseUrl, `{template_path}`, {{ method: "{verb.upper()}", query, token: this.token{body_line} }});
  }}"""
        )

    return f"""// Generated from FastAPI OpenAPI. Do not edit by hand.

function buildUrl(baseUrl, path, query) {{
  const url = new URL(path, baseUrl);
  for (const [key, value] of Object.entries(query || {{}})) {{
    if (value !== undefined && value !== null && value !== "") {{
      url.searchParams.set(key, String(value));
    }}
  }}
  return url;
}}

async function request(baseUrl, path, options = {{}}) {{
  const headers = {{ "content-type": "application/json" }};
  if (options.token) {{
    headers.authorization = `Bearer ${{options.token}}`;
  }}
  const response = await fetch(buildUrl(baseUrl, path, options.query), {{
    method: options.method || "GET",
    headers,
    body: options.body
  }});
  const text = await response.text();
  const data = text ? JSON.parse(text) : null;
  if (!response.ok) {{
    const error = new Error(data?.detail?.message || data?.detail || response.statusText);
    error.status = response.status;
    error.payload = data;
    throw error;
  }}
  return data;
}}

export class ZippyCustomerApi {{
  constructor(baseUrl, token = "") {{
    this.baseUrl = baseUrl.replace(/\\/$/, "");
    this.token = token;
  }}

  setToken(token) {{
    this.token = token;
  }}

{chr(10).join(methods)}
}}
"""


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    openapi = app.openapi()
    (OUT / "openapi.json").write_text(json.dumps(openapi, indent=2), encoding="utf-8")
    (OUT / "generated-types.d.ts").write_text(build_types(openapi), encoding="utf-8")
    (OUT / "generated-client.js").write_text(build_client(openapi), encoding="utf-8")


if __name__ == "__main__":
    main()

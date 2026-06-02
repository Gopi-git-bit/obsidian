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
    ("get", "/api/v1/finance/settlements"): "listSettlements",
    ("get", "/api/v1/finance/settlements/{trip_id}"): "getSettlement",
    ("post", "/api/v1/trips/{trip_id}/settlements/release"): "releaseSettlement",
}


def build_client(openapi):
    methods = []
    for (verb, path), method_name in METHOD_NAMES.items():
        if path not in openapi["paths"] or verb not in openapi["paths"][path]:
            raise RuntimeError(f"OpenAPI path missing: {verb.upper()} {path}")
        params = sorted(set(re.findall(r"{([^}]+)}", path)))
        args = [*params]
        if verb != "get":
            args.append("body")
        args.append("query = {}")
        template_path = re.sub(r"{([^}]+)}", r"${\1}", path)
        body_line = ", body: JSON.stringify(body)" if verb != "get" else ""
        methods.append(f"""  async {method_name}({", ".join(args)}) {{
    return request(this.baseUrl, `{template_path}`, {{ method: "{verb.upper()}", query, token: this.token{body_line} }});
  }}""")
    return f"""// Generated from FastAPI OpenAPI. Do not edit by hand.

function buildUrl(baseUrl, path, query) {{
  const url = new URL(path, baseUrl);
  for (const [key, value] of Object.entries(query || {{}})) {{
    if (value !== undefined && value !== null && value !== "") url.searchParams.set(key, String(value));
  }}
  return url;
}}

async function request(baseUrl, path, options = {{}}) {{
  const headers = {{ "content-type": "application/json" }};
  if (options.token) headers.authorization = `Bearer ${{options.token}}`;
  const response = await fetch(buildUrl(baseUrl, path, options.query), {{ method: options.method || "GET", headers, body: options.body }});
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

export class ZippyFinanceApi {{
  constructor(baseUrl, token = "") {{ this.baseUrl = baseUrl.replace(/\\/$/, ""); this.token = token; }}
  setToken(token) {{ this.token = token; }}

{chr(10).join(methods)}
}}
"""


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    openapi = app.openapi()
    (OUT / "openapi.json").write_text(json.dumps(openapi, indent=2), encoding="utf-8")
    (OUT / "generated-types.d.ts").write_text("// Generated from FastAPI OpenAPI. Do not edit by hand.\n", encoding="utf-8")
    (OUT / "generated-client.js").write_text(build_client(openapi), encoding="utf-8")


if __name__ == "__main__":
    main()

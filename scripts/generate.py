#!/usr/bin/env python3
"""Regenerate MCP configs, registry server.json files and README tool tables
from suites.json, using live data from the public Apify Store API.

    python3 scripts/generate.py            # write files
    python3 scripts/generate.py --check    # fail if a listed tool is not public

No Apify token is needed: only public Store data is read.
Promote a tool from "comingSoon" to "tools" in suites.json once it is public,
then rerun this script and bump "version" before republishing to the MCP Registry.
"""
import json
import pathlib
import re
import sys
import urllib.request
from datetime import date

ROOT = pathlib.Path(__file__).resolve().parent.parent
CFG = json.loads((ROOT / "suites.json").read_text())
OWNER = CFG["owner"]


def store_items():
    url = f"https://api.apify.com/v2/store?username={OWNER}&limit=200"
    with urllib.request.urlopen(url, timeout=30) as r:
        return {i["name"]: i for i in json.load(r)["data"]["items"]}


STORE = store_items()


def mcp_url(tools):
    return CFG["mcpBase"] + "?tools=" + ",".join(f"{OWNER}/{t}" for t in tools)


def tool_name(t):
    return f"{OWNER}--{t}"


def store_url(t):
    return f"https://apify.com/{OWNER}/{t}"


def fmt_usd(x):
    s = f"{x:.5f}".rstrip("0")
    whole, frac = s.split(".")
    return f"${whole}.{frac.ljust(2, '0')}"


KEEP = {"Google", "People", "PageSpeed", "AI", "Amazon", "SERP", "Lighthouse"}


def unit(title):
    first, _, rest = title.partition(" ")
    if first not in KEEP:
        first = first.lower()
    return (first + " " + rest).strip()


def price_cells(name):
    item = STORE[name]
    pi = item.get("currentPricingInfo") or {}
    events = (pi.get("pricingPerEvent") or {}).get("actorChargeEvents") or {}
    def price(ev):
        return ev.get("eventPriceUsd") or ev.get("eventTieredPricingUsd", {}).get("FREE", {}).get("tieredEventPriceUsd")
    primary = [e for e in events.values() if e.get("isPrimaryEvent")] or list(events.values())[:1]
    if not primary:
        return "see Store"
    p = primary[0]
    main = f"{fmt_usd(price(p))} per {unit(p['eventTitle'])}"
    per_k = price(p) * 1000
    if per_k >= 0.5 and price(p) < 0.01:
        main += f" ({fmt_usd(round(per_k, 2))} / 1,000)"
    extras = []
    for k, e in events.items():
        if e is p:
            continue
        if k == "actor-start":
            extras.append(f"{fmt_usd(price(e))} per run start")
        else:
            extras.append(f"{fmt_usd(price(e))} per {unit(e['eventTitle'])}")
    if extras:
        main += "<br><sub>also " + "; ".join(extras) + "</sub>"
    return main


def check():
    bad = []
    for s in CFG["suites"]:
        for t in s["tools"]:
            if t not in STORE:
                bad.append((s["id"], t))
    for t in CFG["more"]:
        if t not in STORE:
            bad.append(("more", t))
    ready = sorted({t for s in CFG["suites"] for t in s["comingSoon"] if t in STORE})
    return bad, ready


def table(tools, with_price=True):
    rows = ["| | Tool (MCP name) | What it returns | Price (Apify Free plan) |", "|---|---|---|---|"]
    for t in tools:
        icon = f'<img src="assets/icons/{t}.png" width="28" alt="">'
        rows.append(
            f"| {icon} | [`{tool_name(t)}`]({store_url(t)}) | {CFG['summaries'][t]} | {price_cells(t)} |"
        )
    return "\n".join(rows)


def soon_list(tools):
    return "\n".join(f"- `{tool_name(t)}`: {CFG['summaries'][t]}" for t in tools)


def write(path, data):
    p = ROOT / path
    p.parent.mkdir(parents=True, exist_ok=True)
    if isinstance(data, (dict, list)):
        data = json.dumps(data, indent=2, ensure_ascii=False) + "\n"
    p.write_text(data)


def server_json(s):
    raw = "https://raw.githubusercontent.com/wrenfielddata/wrenfield-mcp/main"
    doc = {
        "$schema": "https://static.modelcontextprotocol.io/schemas/2025-12-11/server.schema.json",
        "name": f"{CFG['registryNamespace']}/{s['id']}",
        "title": s["registryTitle"],
        "description": s["description"],
        "version": CFG["version"],
        "websiteUrl": CFG["website"],
        "repository": {"url": CFG["repo"], "source": "github", "subfolder": f"registry/{s['id']}"},
        "icons": [{"src": f"{raw}/assets/suites/{s['id']}.png", "mimeType": "image/png", "sizes": ["400x400"]}],
        "remotes": [
            {
                "type": "streamable-http",
                "url": mcp_url(s["tools"]),
                "headers": [
                    {
                        "name": "Authorization",
                        "description": "Optional. 'Bearer <Apify API token>' from Apify Console > Settings > API & Integrations. Omit to sign in with OAuth.",
                        "isRequired": False,
                        "isSecret": True,
                    }
                ],
            }
        ],
        "_meta": {
            "io.modelcontextprotocol.registry/publisher-provided": {
                "host": "Apify MCP server (mcp.apify.com)",
                "tools": [tool_name(t) for t in s["tools"]],
                "pricing": "Pay per result on Apify; no subscription",
                "apifyStore": [store_url(t) for t in s["tools"]],
            }
        },
    }
    meta = json.dumps(doc["_meta"]["io.modelcontextprotocol.registry/publisher-provided"])
    assert len(meta.encode()) < 4096, "publisher-provided _meta over 4 KB"
    assert len(doc["description"]) <= 100
    return doc


def configs():
    suites = CFG["suites"]
    oauth = {"mcpServers": {s["key"]: {"url": mcp_url(s["tools"])} for s in suites}}
    bearer = {"mcpServers": {s["key"]: {"url": mcp_url(s["tools"]), "headers": {"Authorization": "Bearer <YOUR_APIFY_TOKEN>"}} for s in suites}}
    write("configs/generic-oauth.json", oauth)
    write("configs/generic-bearer.json", bearer)
    write("configs/cursor.json", oauth)
    write("configs/claude-desktop.json", {
        "mcpServers": {
            s["key"]: {
                "command": "npx",
                "args": ["-y", "@apify/actors-mcp-server@latest", "--tools", ",".join(f"{OWNER}/{t}" for t in s["tools"])],
                "env": {"APIFY_TOKEN": "<YOUR_APIFY_TOKEN>"},
            } for s in suites
        }
    })
    write("configs/vscode.json", {
        "inputs": [{"type": "promptString", "id": "apify-token", "description": "Apify API token", "password": True}],
        "servers": {
            s["key"]: {"type": "http", "url": mcp_url(s["tools"]), "headers": {"Authorization": "Bearer ${input:apify-token}"}}
            for s in suites
        },
    })
    write("configs/windsurf.json", {"mcpServers": {s["key"]: {"serverUrl": mcp_url(s["tools"]), "headers": {"Authorization": "Bearer <YOUR_APIFY_TOKEN>"}} for s in suites}})
    write("configs/cline.json", {"mcpServers": {s["key"]: {"type": "streamableHttp", "url": mcp_url(s["tools"]), "headers": {"Authorization": "Bearer <YOUR_APIFY_TOKEN>"}} for s in suites}})
    lines = ["#!/usr/bin/env bash", "# Claude Code: add all three Wrenfield servers (needs APIFY_TOKEN in your shell).", "# Drop the --header flag to sign in with OAuth instead (run /mcp in Claude Code).", ""]
    for s in suites:
        lines.append(f'claude mcp add --transport http {s["key"]} "{mcp_url(s["tools"])}" --header "Authorization: Bearer $APIFY_TOKEN"')
    write("configs/claude-code.sh", "\n".join(lines) + "\n")


def replace_block(text, name, body):
    pat = re.compile(rf"<!-- BEGIN:{re.escape(name)} -->.*?<!-- END:{re.escape(name)} -->", re.S)
    if not pat.search(text):
        raise SystemExit(f"README marker {name} missing")
    block = f"<!-- BEGIN:{name} -->\n" + (body + "\n" if body else "") + f"<!-- END:{name} -->"
    return pat.sub(lambda m: block, text)


def readme():
    p = ROOT / "README.md"
    text = p.read_text()
    for s in CFG["suites"]:
        text = replace_block(text, f"url:{s['id']}", f"```text\n{mcp_url(s['tools'])}\n```")
        text = replace_block(text, f"table:{s['id']}", table(s["tools"]))
        soon = [t for t in s["comingSoon"] if t not in s["tools"]]
        text = replace_block(text, f"soon:{s['id']}", ("**Coming soon** (being published on Apify Store this week; not callable yet):\n\n" + soon_list(soon)) if soon else "")
    text = replace_block(text, "table:more", table(CFG["more"]))
    text = replace_block(text, "prices-date", f"<sub>Prices pulled from Apify Store on {date.today().isoformat()}. They are Apify Free-plan rates; paid Apify plans get lower tiered rates. Each Actor's Store page is the authoritative price list. A \"run start\" fee is charged once per call.</sub>")
    p.write_text(text)


def llms_install():
    s0 = CFG["suites"][0]
    body = f"""# llms-install.md: setup notes for AI coding agents (Cline, Claude Code, Cursor, etc.)

These are **remote** MCP servers hosted on the Apify MCP server (`mcp.apify.com`).
Do not clone, build or run anything from this repository.

1. Ask the user which server they want. All three can be added side by side:
"""
    for s in CFG["suites"]:
        body += f"   - **{s['title']}** (`{s['key']}`): `{mcp_url(s['tools'])}`\n"
    body += f"""2. Authentication: if the client supports remote MCP OAuth, add only the URL and the user signs in to Apify in the browser.
   Otherwise ask the user for an Apify API token (Apify Console > Settings > API & Integrations) and send it as
   the header `Authorization: Bearer <token>`. Never write the token into a file that is committed to git.
3. Add the server to the client's MCP settings, for example:

```json
{{
  "mcpServers": {{
    "{s0['key']}": {{
      "url": "{mcp_url(s0['tools'])}",
      "headers": {{ "Authorization": "Bearer <APIFY_TOKEN>" }}
    }}
  }}
}}
```

   For Cline, add `"type": "streamableHttp"` next to `url`. Ready-made files for other clients are in `configs/`.
4. Verify by listing tools. Expect {", ".join(f"`{tool_name(t)}`" for t in s0['tools'])}
   plus Apify helper tools (`get-actor-run`, `get-dataset-items`, `get-key-value-store-record`, `abort-actor-run`).
5. Every tool call is billed per result to the user's Apify account. Ask before large runs. The per-Actor
   tools above take only the Actor input and have no spend-cap argument. To cap the spend of a single run,
   add `call-actor` to the URL's `tools=` list and call it with the Actor name, its `input`, and
   `callOptions.maxTotalChargeUsd`. `call-actor` returns the run status and dataset ID; read the rows with
   `get-dataset-items`.
6. HTTP 401 means the token is missing or invalid.
"""
    write("llms-install.md", body)


if __name__ == "__main__":
    bad, ready = check()
    if bad:
        print("NOT PUBLIC on Apify Store:", bad)
        sys.exit(1)
    if ready:
        print("Now public, can be promoted from comingSoon:", ready)
    if "--check" in sys.argv:
        print("OK: every listed tool is public")
        sys.exit(0)
    for s in CFG["suites"]:
        write(f"registry/{s['id']}/server.json", server_json(s))
    configs()
    readme()
    llms_install()
    print("generated")

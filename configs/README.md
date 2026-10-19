# Client configs

Each file defines all three Wrenfield servers (`wrenfield-seo`, `wrenfield-ai-search`, `wrenfield-leads`). Keep the ones you need. Replace `<YOUR_APIFY_TOKEN>` with a token from [Apify Console → Settings → API & Integrations](https://console.apify.com/settings/integrations), or use the OAuth variants and sign in to Apify in your browser instead. Don't commit a file that contains a real token.

These files are generated from `../suites.json` by `../scripts/generate.py`.

| File | Client | Where it goes | Auth |
|---|---|---|---|
| `generic-oauth.json` | Any client that supports remote MCP | the client's MCP settings | OAuth |
| `generic-bearer.json` | Any client that supports remote MCP | the client's MCP settings | Bearer token |
| `cursor.json` | Cursor | `~/.cursor/mcp.json` or `<project>/.cursor/mcp.json` | OAuth (add `headers` for a token) |
| `vscode.json` | VS Code / GitHub Copilot | `<project>/.vscode/mcp.json` | Bearer token, prompted once (remove `headers` for OAuth) |
| `claude-desktop.json` | Claude Desktop | `claude_desktop_config.json` (Settings → Developer → Edit Config) | Token, via Apify's local stdio server (needs Node 18+) |
| `claude-code.sh` | Claude Code | run it in a shell with `APIFY_TOKEN` set | Bearer token (drop `--header` for OAuth) |
| `windsurf.json` | Windsurf | `~/.codeium/windsurf/mcp_config.json` | Bearer token |
| `cline.json` | Cline | Cline → MCP Servers → Configure | Bearer token |

**Claude Desktop with no local install:** go to Settings → Connectors → *Add custom connector* and paste a suite URL from the main README. Availability depends on your Claude plan.

**ChatGPT:** where custom MCP connectors (developer mode) are enabled for your plan or workspace, create a custom MCP app or connector, paste a suite URL and choose OAuth. See the main README.

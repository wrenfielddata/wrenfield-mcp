# llms-install.md: setup notes for AI coding agents (Cline, Claude Code, Cursor, etc.)

These are **remote** MCP servers hosted on the Apify MCP server (`mcp.apify.com`).
Do not clone, build or run anything from this repository.

1. Ask the user which server they want. All three can be added side by side:
   - **Wrenfield SEO Data** (`wrenfield-seo`): `https://mcp.apify.com?tools=wrenfield-data/keyword-search-volume,wrenfield-data/domain-authority-traffic-checker,wrenfield-data/google-trends-scraper,wrenfield-data/google-ads-transparency-scraper`
   - **Wrenfield AI Search Visibility** (`wrenfield-ai-search`): `https://mcp.apify.com?tools=wrenfield-data/ai-search-visibility-tracker,wrenfield-data/keyword-search-volume`
   - **Wrenfield Local Leads** (`wrenfield-leads`): `https://mcp.apify.com?tools=wrenfield-data/website-contact-scraper,wrenfield-data/website-tech-stack-detector,wrenfield-data/company-name-to-domain`
2. Authentication: if the client supports remote MCP OAuth, add only the URL and the user signs in to Apify in the browser.
   Otherwise ask the user for an Apify API token (Apify Console > Settings > API & Integrations) and send it as
   the header `Authorization: Bearer <token>`. Never write the token into a file that is committed to git.
3. Add the server to the client's MCP settings, for example:

```json
{
  "mcpServers": {
    "wrenfield-seo": {
      "url": "https://mcp.apify.com?tools=wrenfield-data/keyword-search-volume,wrenfield-data/domain-authority-traffic-checker,wrenfield-data/google-trends-scraper,wrenfield-data/google-ads-transparency-scraper",
      "headers": { "Authorization": "Bearer <APIFY_TOKEN>" }
    }
  }
}
```

   For Cline, add `"type": "streamableHttp"` next to `url`. Ready-made files for other clients are in `configs/`.
4. Verify by listing tools. Expect `wrenfield-data--keyword-search-volume`, `wrenfield-data--domain-authority-traffic-checker`, `wrenfield-data--google-trends-scraper`, `wrenfield-data--google-ads-transparency-scraper`
   plus Apify helper tools (`get-actor-run`, `get-dataset-items`, `get-key-value-store-record`, `abort-actor-run`).
5. Every tool call is billed per result to the user's Apify account. Ask before large runs, and pass
   `callOptions.maxTotalChargeUsd` to cap the spend of a single call.
6. HTTP 401 means the token is missing or invalid.

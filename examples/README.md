# Examples

All examples call Wrenfield Data Actors through the Apify API and need `APIFY_TOKEN` set in your environment (from [Apify Console → Settings → API & Integrations](https://console.apify.com/settings/integrations)). Each call is billed per result to your Apify account, and every example caps spend with `maxTotalChargeUsd`.

| File | Actor | Approx. cost per run* |
|---|---|---|
| `curl/keyword-search-volume.sh` | keyword-search-volume | 2 keywords × $0.004, plus one Keyword Planner request fee (see Store) |
| `curl/ai-search-visibility.sh` | ai-search-visibility-tracker | 1 prompt × 2 engines × $0.04 = $0.08 |
| `curl/tech-stack.sh` | website-tech-stack-detector | 2 sites × $0.0025 |
| `python/run_sync.py` | domain-authority-traffic-checker (`requests`) | 2 domains × $0.005 + $0.001 |
| `python/apify_client_example.py` | company-name-to-domain (`apify-client`) | 3 companies × $0.0015 |
| `node/run-sync.mjs` | website-contact-scraper (`fetch`) | websites with contacts × $0.004 |
| `node/apify-client.mjs` | keyword-search-volume (`apify-client`) | as above |

\*Apify Free-plan rates on 2026-10-19. The Actor's Store page has the current prices.

`run-sync-get-dataset-items` waits up to 300 seconds. For bigger jobs, start a run and poll it, or use `apify-client`'s `.call()`, which waits for you.

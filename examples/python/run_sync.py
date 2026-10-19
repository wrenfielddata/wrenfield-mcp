"""Domain authority and organic traffic for a few domains, using plain `requests`.

    pip install requests
    APIFY_TOKEN=... python run_sync.py
"""
import os

import requests

ACTOR = "wrenfield-data~domain-authority-traffic-checker"

resp = requests.post(
    f"https://api.apify.com/v2/acts/{ACTOR}/run-sync-get-dataset-items",
    params={"maxTotalChargeUsd": 1},
    headers={"Authorization": f"Bearer {os.environ['APIFY_TOKEN']}"},
    json={"domains": ["hubspot.com", "pipedrive.com"]},
    timeout=320,
)
resp.raise_for_status()

for row in resp.json():
    print(f"{row['domain']:<20} rank={row.get('domain_rank')} organic_traffic={row.get('organic_traffic')}")

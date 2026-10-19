"""Resolve company names to official domains with the official Apify Python client.

    pip install apify-client
    APIFY_TOKEN=... python apify_client_example.py
"""
import os

from apify_client import ApifyClient

client = ApifyClient(os.environ["APIFY_TOKEN"])

run = client.actor("wrenfield-data/company-name-to-domain").call(
    run_input={"companies": ["Stripe", "Patagonia", "Mercury | banking for startups"]},
)

for item in client.dataset(run["defaultDatasetId"]).iterate_items():
    print(item)

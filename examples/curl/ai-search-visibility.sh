#!/usr/bin/env bash
# Does ChatGPT / Google AI Mode mention HubSpot for this prompt, and which URLs are cited?
set -euo pipefail
curl -sS -X POST \
  "https://api.apify.com/v2/acts/wrenfield-data~ai-search-visibility-tracker/run-sync-get-dataset-items?maxTotalChargeUsd=1" \
  -H "Authorization: Bearer ${APIFY_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "brands": ["HubSpot"],
    "domains": ["hubspot.com"],
    "competitors": ["Salesforce | salesforce.com", "Pipedrive | pipedrive.com"],
    "prompts": ["What is the best CRM for a small business?"],
    "engines": ["chatgpt", "google_ai_mode"],
    "country": "United States"
  }'

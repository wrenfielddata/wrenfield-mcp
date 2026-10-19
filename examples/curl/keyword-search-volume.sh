#!/usr/bin/env bash
# Google search volume, CPC and 12-month trend for a few keywords.
set -euo pipefail
curl -sS -X POST \
  "https://api.apify.com/v2/acts/wrenfield-data~keyword-search-volume/run-sync-get-dataset-items?maxTotalChargeUsd=1" \
  -H "Authorization: Bearer ${APIFY_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "keywords": ["crm software", "free crm"],
    "mode": "search_volume",
    "location": "United States",
    "language": "English"
  }'

#!/usr/bin/env bash
# Technologies detected on a couple of websites.
set -euo pipefail
curl -sS -X POST \
  "https://api.apify.com/v2/acts/wrenfield-data~website-tech-stack-detector/run-sync-get-dataset-items?maxTotalChargeUsd=0.5" \
  -H "Authorization: Bearer ${APIFY_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{"urls": ["wordpress.org", "allbirds.com"]}'

#!/usr/bin/env bash
# Claude Code: add all three Wrenfield servers (needs APIFY_TOKEN in your shell).
# Drop the --header flag to sign in with OAuth instead (run /mcp in Claude Code).

claude mcp add --transport http wrenfield-seo "https://mcp.apify.com?tools=wrenfield-data/keyword-search-volume,wrenfield-data/domain-authority-traffic-checker,wrenfield-data/google-trends-scraper,wrenfield-data/google-ads-transparency-scraper,wrenfield-data/competitor-keywords,wrenfield-data/keyword-difficulty-checker,wrenfield-data/keyword-research-tool,wrenfield-data/seo-toolkit,wrenfield-data/google-autocomplete-keyword-expander,wrenfield-data/people-also-ask-scraper" --header "Authorization: Bearer $APIFY_TOKEN"
claude mcp add --transport http wrenfield-ai-search "https://mcp.apify.com?tools=wrenfield-data/ai-search-visibility-tracker,wrenfield-data/keyword-search-volume,wrenfield-data/people-also-ask-scraper,wrenfield-data/ai-answer-scraper,wrenfield-data/agency-ai-visibility-reports" --header "Authorization: Bearer $APIFY_TOKEN"
claude mcp add --transport http wrenfield-leads "https://mcp.apify.com?tools=wrenfield-data/website-contact-scraper,wrenfield-data/website-tech-stack-detector,wrenfield-data/company-name-to-domain" --header "Authorization: Bearer $APIFY_TOKEN"

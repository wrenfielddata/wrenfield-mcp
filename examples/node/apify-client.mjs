// Keyword search volume with the official Apify JS client.
//   npm install apify-client
//   APIFY_TOKEN=... node apify-client.mjs
import { ApifyClient } from "apify-client";

const client = new ApifyClient({ token: process.env.APIFY_TOKEN });

const run = await client.actor("wrenfield-data/keyword-search-volume").call({
  keywords: ["crm software", "free crm"],
  mode: "search_volume",
  location: "United States",
  language: "English",
});

const { items } = await client.dataset(run.defaultDatasetId).listItems();
for (const k of items) console.log(k.keyword, k.search_volume, k.cpc);

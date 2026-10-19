// Emails, phones and social profiles from company websites (Node 18+, no dependencies).
//   APIFY_TOKEN=... node run-sync.mjs
const ACTOR = "wrenfield-data~website-contact-scraper";

const res = await fetch(
  `https://api.apify.com/v2/acts/${ACTOR}/run-sync-get-dataset-items?maxTotalChargeUsd=0.5`,
  {
    method: "POST",
    headers: {
      Authorization: `Bearer ${process.env.APIFY_TOKEN}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ urls: ["apify.com", "levainbakery.com"] }),
  },
);
if (!res.ok) throw new Error(`${res.status} ${await res.text()}`);

for (const row of await res.json()) console.log(JSON.stringify(row, null, 2));

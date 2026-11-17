# Document readers (Cloudflare Worker)

One Worker serves three readers:

| Address | Used by | Reads | Model |
|---|---|---|---|
| `/read` | Carbon Jigsaw | Bills: kWh, litres, m³, supplier, billing period | `MODEL` (Haiku) |
| `/sds` | Safety Data Sheet Checker | Safety data sheets: product, supplier, date, substances with CAS numbers | `MODEL` (Haiku) |
| `/site` | Site Report Reader | Land and ground reports: history, risks, results, recommendations | `MODEL_SITE` (Sonnet) |

The bill reader returns only the figures (kWh, litres, cubic metres, supplier, billing period). It stores no bills. The only data it keeps is a daily counter per visitor, keyed by a salted hash of their IP address and deleted after two days, plus a monthly total.

The Jigsaw hides the "Read it from my bill" option until `BILL_API` is set in `tools/carbon-jigsaw.html`, so nothing changes on the live site until the steps below are done.

## One-off set-up (about 15 minutes)

You need a free Cloudflare account and Node.js on your Mac.

1. **API key.** In the Claude Console (platform.claude.com), create an API key for a workspace that draws on your monthly credits. Under **Limits**, set a monthly spend limit for that workspace, for example $20, so the bill reader can never run past it.
2. **Log in to Cloudflare** from this folder:
   ```
   cd workers/bill-reader
   npx wrangler login
   ```
3. **Create the counter store** and paste the id it prints into `wrangler.toml` in place of `PASTE_KV_NAMESPACE_ID_HERE`:
   ```
   npx wrangler kv namespace create RL
   ```
4. **Add the secrets** (each command asks you to paste the value):
   ```
   npx wrangler secret put ANTHROPIC_API_KEY
   npx wrangler secret put IP_SALT
   ```
   For `IP_SALT`, paste any long random phrase. It stops the IP hashes being reversed.
5. **Deploy:**
   ```
   npx wrangler deploy
   ```
   Wrangler prints the address, e.g. `https://rjp-bill-reader.<your-subdomain>.workers.dev`.
6. **Switch it on.** In `tools/carbon-jigsaw.html`, set
   ```
   const BILL_API="https://rjp-bill-reader.<your-subdomain>.workers.dev/read";
   ```
   and merge. The privacy page already describes the readers.
7. **Switch on the other two readers.** In `tools/sds-checker.html` and `tools/site-report-reader.html`, set
   ```
   const READER_BASE="https://rjp-bill-reader.<your-subdomain>.workers.dev";
   ```
   (no `/read` on the end) and merge.

## Settings

In `wrangler.toml`:

- `DAILY_LIMIT`: bills, and separately safety data sheets, per visitor per day (default 5).
- `DAILY_LIMIT_SITE`: site reports per visitor per day (default 3). Site reports are long, so each costs more to read.
- `MONTHLY_LIMIT`: documents per month across all three readers (default 1,000). The Console spend limit is the hard backstop.
- `MODEL`: defaults to `claude-haiku-5-5`, which is quick and cheap for reading figures. Change it to `claude-sonnet-5-5` if photos of poor-quality bills are misread.
- `MODEL_SITE`: defaults to `claude-sonnet-5-5` for site reports, which need careful reading. A long report costs noticeably more than a bill, which is why it has its own lower daily limit.
- `ALLOWED_ORIGINS`: only pages on these addresses can use the Worker.

Logging is turned off (`[observability] enabled = false`), so bills never appear in Cloudflare's logs. Leave it off.

## What leaves the visitor's device

The bill (images are shrunk to 1,600 pixels on the visitor's device first) goes to this Worker and on to Anthropic's API. Anthropic deletes API inputs and outputs within 30 days, keeps them longer only to enforce its usage policy or by law, and does not train its models on them. The Worker returns only the figures. Nothing is written to the site or sent to Robert.

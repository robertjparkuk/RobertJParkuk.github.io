# Bill reader (Cloudflare Worker)

Reads a photo or PDF of a bill for the Carbon Jigsaw and returns only the figures (kWh, litres, cubic metres, supplier, billing period). It stores no bills. The only data it keeps is a daily counter per visitor, keyed by a salted hash of their IP address and deleted after two days, plus a monthly total.

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
   and merge. The privacy page already describes the bill reader.

## Settings

In `wrangler.toml`:

- `DAILY_LIMIT`: bills per visitor per day (default 5).
- `MONTHLY_LIMIT`: bills per month for the whole site (default 1,000). The Console spend limit is the hard backstop.
- `MODEL`: defaults to `claude-haiku-5-5`, which is quick and cheap for reading figures. Change it to `claude-sonnet-5-5` if photos of poor-quality bills are misread.
- `ALLOWED_ORIGINS`: only pages on these addresses can use the Worker.

Logging is turned off (`[observability] enabled = false`), so bills never appear in Cloudflare's logs. Leave it off.

## What leaves the visitor's device

The bill (images are shrunk to 1,600 pixels on the visitor's device first) goes to this Worker and on to Anthropic's API. Anthropic deletes API inputs and outputs within 30 days, keeps them longer only to enforce its usage policy or by law, and does not train its models on them. The Worker returns only the figures. Nothing is written to the site or sent to Robert.

// Bill reader for the Carbon Jigsaw.
//
// The page sends one bill (a photo or a PDF) here. This Worker checks where the
// request came from and how many bills have been read today, sends the bill to
// Claude to read, and returns only the figures. It stores no bills and no
// figures. The only thing it keeps is a counter: a salted hash of the visitor's
// IP address (deleted after two days) and a monthly total.
//
// Secrets (set with `wrangler secret put`): ANTHROPIC_API_KEY, IP_SALT
// Variables (wrangler.toml): ALLOWED_ORIGINS, MODEL, DAILY_LIMIT, MONTHLY_LIMIT
// KV binding: RL

const MAX_BYTES = 4 * 1024 * 1024; // 4 MB after decoding
const TYPES = ["image/jpeg", "image/png", "image/webp", "image/gif", "application/pdf"];
const KINDS = ["elec", "gas", "oil", "water"];

const TOOL = {
  name: "record_bill",
  description: "Record the figures read from a UK or Irish utility bill, fuel delivery docket or water bill.",
  input_schema: {
    type: "object",
    properties: {
      is_bill: { type: "boolean", description: "False if this is not a utility bill, fuel docket or water bill, or is unreadable." },
      bill_type: { type: "string", enum: ["electricity", "gas", "heating_oil", "water", "other"] },
      supplier: { type: ["string", "null"], description: "Supplier or company name as printed, e.g. Power NI, SSE Airtricity, firmus energy, NI Water." },
      period_start: { type: ["string", "null"], description: "Start of the billing period, YYYY-MM-DD." },
      period_end: { type: ["string", "null"], description: "End of the billing period, YYYY-MM-DD." },
      kwh: { type: ["number", "null"], description: "Total energy used in the period in kWh (for gas, the kWh figure, not cubic metres). Use the annual total only if no period figure is shown." },
      kwh_is_annual: { type: "boolean", description: "True if kwh is a printed 12-month total rather than the period's usage." },
      litres_kerosene: { type: ["number", "null"], description: "Litres of kerosene / heating oil / 28-second oil delivered." },
      litres_gas_oil: { type: ["number", "null"], description: "Litres of gas oil / red diesel / 35-second oil delivered." },
      litres_lpg: { type: ["number", "null"], description: "Litres of LPG delivered." },
      water_m3: { type: ["number", "null"], description: "Water supplied in cubic metres for the period." },
      sewer_m3: { type: ["number", "null"], description: "Wastewater / sewerage volume in cubic metres for the period." },
      notes: { type: ["string", "null"], description: "One short sentence if anything is unclear, e.g. an estimated read. No personal details." }
    },
    required: ["is_bill", "bill_type"]
  }
};

const PROMPT = `Read this bill and record its figures with the record_bill tool.
Rules:
- Only record numbers printed on the bill. Never estimate or calculate a figure that is not shown, except adding up the lines of a single bill.
- Do not record names, addresses, account numbers, meter numbers or any other personal details anywhere, including notes.
- If a figure is not shown, use null.
- Electricity and gas: record kWh used in this billing period. If only a 12-month total is shown, record that and set kwh_is_annual true.
- Heating oil, gas oil or LPG docket: record litres delivered.
- Water bill: record supply and sewerage volumes in cubic metres.`;

function cors(origin) {
  return {
    "Access-Control-Allow-Origin": origin,
    "Access-Control-Allow-Methods": "POST, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type",
    "Access-Control-Max-Age": "86400",
    "Vary": "Origin"
  };
}

function reply(status, body, origin) {
  return new Response(JSON.stringify(body), {
    status,
    headers: { "Content-Type": "application/json", "Cache-Control": "no-store", ...(origin ? cors(origin) : {}) }
  });
}

async function sha256(text) {
  const buf = await crypto.subtle.digest("SHA-256", new TextEncoder().encode(text));
  return [...new Uint8Array(buf)].map(b => b.toString(16).padStart(2, "0")).join("");
}

function decodedSize(b64) {
  const pad = b64.endsWith("==") ? 2 : b64.endsWith("=") ? 1 : 0;
  return Math.floor(b64.length * 3 / 4) - pad;
}

const num = v => (typeof v === "number" && isFinite(v) && v >= 0 ? v : null);
const date = v => (typeof v === "string" && /^\d{4}-\d{2}-\d{2}$/.test(v) ? v : null);
const text = (v, n) => (typeof v === "string" && v.trim() ? v.trim().slice(0, n) : null);

// Keep only the expected fields, in the expected shapes.
export function clean(r) {
  return {
    is_bill: r.is_bill === true,
    bill_type: ["electricity", "gas", "heating_oil", "water", "other"].includes(r.bill_type) ? r.bill_type : "other",
    supplier: text(r.supplier, 60),
    period_start: date(r.period_start),
    period_end: date(r.period_end),
    kwh: num(r.kwh),
    kwh_is_annual: r.kwh_is_annual === true,
    litres_kerosene: num(r.litres_kerosene),
    litres_gas_oil: num(r.litres_gas_oil),
    litres_lpg: num(r.litres_lpg),
    water_m3: num(r.water_m3),
    sewer_m3: num(r.sewer_m3),
    notes: text(r.notes, 200)
  };
}

export default {
  async fetch(request, env) {
    const origin = request.headers.get("Origin") || "";
    const allowed = (env.ALLOWED_ORIGINS || "").split(",").map(s => s.trim()).filter(Boolean);
    const ok = allowed.includes(origin);

    if (request.method === "OPTIONS") return ok ? new Response(null, { status: 204, headers: cors(origin) }) : new Response(null, { status: 403 });
    if (!ok) return reply(403, { error: "This service only works from robertjpark.co.uk." });
    if (request.method !== "POST" || new URL(request.url).pathname !== "/read") return reply(404, { error: "Not found." }, origin);

    let body;
    try { body = await request.json(); } catch { return reply(400, { error: "The upload didn't arrive in a form I can read." }, origin); }
    const { kind, mediaType, data } = body || {};
    if (!KINDS.includes(kind)) return reply(400, { error: "Unknown bill type." }, origin);
    if (!TYPES.includes(mediaType)) return reply(415, { error: "Please upload a photo (JPEG, PNG, WebP) or a PDF." }, origin);
    if (typeof data !== "string" || !data.length) return reply(400, { error: "No file was received." }, origin);
    if (decodedSize(data) > MAX_BYTES) return reply(413, { error: "That file is over 4 MB. Try a photo of the page with the figures, or a smaller PDF." }, origin);

    // Limits: per visitor per day, and a monthly total for the whole site.
    const day = new Date().toISOString().slice(0, 10), month = day.slice(0, 7);
    const ip = request.headers.get("CF-Connecting-IP") || "unknown";
    const dKey = `d:${day}:${await sha256((env.IP_SALT || "") + ip + day)}`;
    const mKey = `m:${month}`;
    const [dCount, mCount] = await Promise.all([env.RL.get(dKey), env.RL.get(mKey)]).then(v => v.map(x => parseInt(x || "0", 10)));
    if (dCount >= parseInt(env.DAILY_LIMIT || "5", 10)) return reply(429, { error: "You've reached today's limit for reading bills. Type the figures in, or try again tomorrow." }, origin);
    if (mCount >= parseInt(env.MONTHLY_LIMIT || "1000", 10)) return reply(429, { error: "The bill reader has reached its limit for this month. Please type the figures in." }, origin);
    await Promise.all([
      env.RL.put(dKey, String(dCount + 1), { expirationTtl: 172800 }),
      env.RL.put(mKey, String(mCount + 1), { expirationTtl: 3456000 })
    ]);

    const file = mediaType === "application/pdf"
      ? { type: "document", source: { type: "base64", media_type: mediaType, data } }
      : { type: "image", source: { type: "base64", media_type: mediaType, data } };

    let res;
    try {
      res = await fetch("https://api.anthropic.com/v1/messages", {
        method: "POST",
        headers: { "x-api-key": env.ANTHROPIC_API_KEY, "anthropic-version": "2023-06-01", "content-type": "application/json" },
        body: JSON.stringify({
          model: env.MODEL || "claude-haiku-5-5",
          max_tokens: 800,
          tools: [TOOL],
          tool_choice: { type: "tool", name: TOOL.name },
          messages: [{ role: "user", content: [file, { type: "text", text: PROMPT }] }]
        })
      });
    } catch {
      return reply(502, { error: "The bill reader couldn't be reached. Please type the figures in." }, origin);
    }
    if (!res.ok) return reply(502, { error: "The bill reader couldn't read that file. Please type the figures in." }, origin);

    const out = await res.json();
    const use = (out.content || []).find(c => c.type === "tool_use" && c.name === TOOL.name);
    if (!use) return reply(502, { error: "The bill reader couldn't find any figures. Please type them in." }, origin);
    return reply(200, { kind, result: clean(use.input || {}) }, origin);
  }
};

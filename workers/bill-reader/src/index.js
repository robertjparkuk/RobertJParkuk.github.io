// Document readers for robertjpark.co.uk:
//   POST /read  bills for the Carbon Jigsaw
//   POST /sds   safety data sheets for the Safety Data Sheet Checker
//   POST /site  land and site reports for the Site Report Reader
//
// The page sends one document (a photo or a PDF) here. This Worker checks where the
// request came from and how many bills have been read today, sends the bill to
// Claude to read, and returns only the figures. It stores no bills and no
// figures. The only thing it keeps is a counter: a salted hash of the visitor's
// IP address (deleted after two days) and a monthly total.
//
// Secrets (set with `wrangler secret put`): ANTHROPIC_API_KEY, IP_SALT
// Variables (wrangler.toml): ALLOWED_ORIGINS, MODEL, MODEL_SITE, DAILY_LIMIT, DAILY_LIMIT_SITE, MONTHLY_LIMIT
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

const SDS_TOOL = {
  name: "record_sds",
  description: "Record the identity and composition of a product from its safety data sheet.",
  input_schema: {
    type: "object",
    properties: {
      is_sds: { type: "boolean", description: "False if this is not a safety data sheet (or is unreadable)." },
      product_name: { type: ["string", "null"] },
      supplier: { type: ["string", "null"], description: "Company that issued the SDS (section 1)." },
      sds_date: { type: ["string", "null"], description: "Revision or issue date as YYYY-MM-DD if shown." },
      sds_format: { type: ["string", "null"], description: "E.g. EU REACH Annex II, UK REACH, GHS, US OSHA, as stated or evident." },
      uses: { type: ["string", "null"], description: "Identified uses from section 1, briefly." },
      product_type: { type: "string", enum: ["substance", "mixture", "article", "unknown"] },
      substances: {
        type: "array", maxItems: 40,
        items: {
          type: "object",
          properties: {
            name: { type: "string" },
            cas: { type: ["string", "null"], description: "CAS number exactly as printed, e.g. 7664-41-7." },
            ec: { type: ["string", "null"], description: "EC number as printed." },
            concentration: { type: ["string", "null"], description: "As printed, e.g. '10 - <25 %'." },
            h_statements: { type: "array", items: { type: "string" }, description: "Hazard statement codes for this substance, e.g. H314." },
            fluorinated: { type: "boolean", description: "True if the substance's structure contains at least one fully fluorinated methyl (CF3-) or methylene (-CF2-) carbon atom without any H, Cl, Br or I attached. False if not or unknown." }
          },
          required: ["name"]
        }
      },
      mixture_h_statements: { type: "array", items: { type: "string" }, description: "Hazard statement codes for the product as a whole (section 2)." },
      svhc_declared: { type: "array", items: { type: "string" }, description: "Any substances the SDS itself says are SVHCs or on the Candidate List." },
      section15: { type: "array", items: { type: "string" }, description: "Regulations named in section 15, short form." },
      notes: { type: ["string", "null"], description: "One short sentence if the composition is withheld, incomplete or unclear. No personal details." }
    },
    required: ["is_sds", "substances"]
  }
};

const SDS_PROMPT = `Read this safety data sheet and record it with the record_sds tool.
Rules:
- Record only what is printed. Copy CAS and EC numbers exactly. Never invent a CAS number; use null if none is printed.
- List every substance in the composition section (section 3), including impurities shown there.
- Do not record names, phone numbers or email addresses of people.`;

const SITE_TOOL = {
  name: "record_site_report",
  description: "Summarise a land contamination or ground investigation report.",
  input_schema: {
    type: "object",
    properties: {
      is_site_report: { type: "boolean", description: "False if this is not a land, ground or contamination report." },
      report_type: { type: "string", enum: ["phase1_desk_study", "phase2_site_investigation", "generic_quantitative_risk_assessment", "detailed_risk_assessment", "remediation_strategy", "verification_report", "ground_gas_assessment", "other"] },
      consultant: { type: ["string", "null"], description: "Company that wrote the report." },
      report_date: { type: ["string", "null"], description: "YYYY-MM-DD if shown." },
      location: { type: ["string", "null"], description: "Town or townland and council area only. No street address or postcode." },
      current_use: { type: ["string", "null"] },
      proposed_use: { type: ["string", "null"], description: "E.g. residential with gardens, commercial, public open space." },
      site_history: { type: "array", items: { type: "string" }, maxItems: 12, description: "Past uses that matter for contamination, with dates if given." },
      contaminants_of_concern: { type: "array", items: { type: "string" }, maxItems: 25 },
      linkages: {
        type: "array", maxItems: 20, description: "Pollutant linkages from the conceptual site model.",
        items: { type: "object", properties: {
          source: { type: "string" }, pathway: { type: "string" }, receptor: { type: "string" },
          risk: { type: ["string", "null"], description: "Risk rating as printed, e.g. Low, Moderate, High." } },
          required: ["source", "pathway", "receptor"] }
      },
      investigation: { type: ["string", "null"], description: "What was done, as printed: number of boreholes, trial pits, wells, depths, monitoring rounds." },
      exceedances: {
        type: "array", maxItems: 30, description: "Results above the screening criteria, only where the report states them.",
        items: { type: "object", properties: {
          medium: { type: "string", enum: ["soil", "groundwater", "surface_water", "leachate", "ground_gas", "vapour", "other"] },
          contaminant: { type: "string" }, max_value: { type: ["string", "null"] }, unit: { type: ["string", "null"] },
          criterion: { type: ["string", "null"], description: "Screening value and its name as printed, e.g. 'C4SL residential 80 mg/kg'." },
          samples: { type: ["string", "null"], description: "How many samples exceeded, if stated." } },
          required: ["medium", "contaminant"] }
      },
      ground_gas: { type: ["string", "null"], description: "Characteristic situation or gas regime as printed, e.g. CS2, and the protection recommended." },
      groundwater: { type: ["string", "null"], description: "Depth, flow direction and any risk to controlled waters, briefly." },
      conclusions: { type: "array", items: { type: "string" }, maxItems: 10 },
      recommendations: { type: "array", items: { type: "string" }, maxItems: 12 },
      remediation: { type: "array", items: { type: "string" }, maxItems: 10, description: "Remediation measures proposed or completed." },
      further_work: { type: "array", items: { type: "string" }, maxItems: 10 },
      guidance_cited: { type: "array", items: { type: "string" }, maxItems: 12, description: "Guidance or standards named, e.g. LCRM, BS 10175, BS 8485, CIRIA C665." },
      limitations: { type: "array", items: { type: "string" }, maxItems: 6 },
      notes: { type: ["string", "null"], description: "One short sentence if pages seem missing or the report is a summary only." }
    },
    required: ["is_site_report", "report_type"]
  }
};

const SITE_PROMPT = `Read this land contamination or ground investigation report and record it with the record_site_report tool.
Rules:
- Record only what the report says. Copy values, units and screening criteria exactly. Never add your own screening values or risk ratings.
- Keep each list item to one short sentence.
- Do not record people's names, street addresses, postcodes, grid references, phone numbers or email addresses. Give location as town or townland and council area only.`;

const ROUTES = {
  "/read": { tool: TOOL, prompt: PROMPT, kinds: KINDS, max: MAX_BYTES, model: env => env.MODEL || "claude-haiku-5-5", daily: env => env.DAILY_LIMIT || "5", maxTokens: 800 },
  "/sds": { tool: SDS_TOOL, prompt: SDS_PROMPT, kinds: ["sds"], max: 8 * 1024 * 1024, model: env => env.MODEL || "claude-haiku-5-5", daily: env => env.DAILY_LIMIT || "5", maxTokens: 3000 },
  "/site": { tool: SITE_TOOL, prompt: SITE_PROMPT, kinds: ["site"], max: 20 * 1024 * 1024, model: env => env.MODEL_SITE || "claude-sonnet-5-5", daily: env => env.DAILY_LIMIT_SITE || "3", maxTokens: 4000 }
};

// Shallow clean for the SDS and site readers: drop unknown keys, trim strings, cap lists.
function tidy(v, depth = 0) {
  if (typeof v === "string") return v.trim().slice(0, 400);
  if (typeof v === "number" || typeof v === "boolean" || v === null) return v;
  if (Array.isArray(v)) return v.slice(0, 40).map(x => tidy(x, depth + 1));
  if (v && typeof v === "object" && depth < 4) return Object.fromEntries(Object.entries(v).map(([k, x]) => [k, tidy(x, depth + 1)]));
  return null;
}
function cleanTo(schema, r) {
  const out = {};
  for (const k of Object.keys(schema.input_schema.properties)) out[k] = k in r ? tidy(r[k]) : null;
  return out;
}

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
    const path = new URL(request.url).pathname, route = ROUTES[path];
    if (request.method !== "POST" || !route) return reply(404, { error: "Not found." }, origin);

    let body;
    try { body = await request.json(); } catch { return reply(400, { error: "The upload didn't arrive in a form I can read." }, origin); }
    const { kind, mediaType, data } = body || {};
    if (!route.kinds.includes(kind)) return reply(400, { error: "Unknown document type." }, origin);
    if (!TYPES.includes(mediaType)) return reply(415, { error: "Please upload a photo (JPEG, PNG, WebP) or a PDF." }, origin);
    if (typeof data !== "string" || !data.length) return reply(400, { error: "No file was received." }, origin);
    if (decodedSize(data) > route.max) return reply(413, { error: `That file is over ${route.max / 1048576} MB. Try a smaller PDF, or only the pages that matter.` }, origin);

    // Limits: per visitor per day, and a monthly total for the whole site.
    const day = new Date().toISOString().slice(0, 10), month = day.slice(0, 7);
    const ip = request.headers.get("CF-Connecting-IP") || "unknown";
    const dKey = `d${path}:${day}:${await sha256((env.IP_SALT || "") + ip + day)}`;
    const mKey = `m:${month}`;
    const [dCount, mCount] = await Promise.all([env.RL.get(dKey), env.RL.get(mKey)]).then(v => v.map(x => parseInt(x || "0", 10)));
    if (dCount >= parseInt(route.daily(env), 10)) return reply(429, { error: "You've reached today's limit for this reader. Please try again tomorrow." }, origin);
    if (mCount >= parseInt(env.MONTHLY_LIMIT || "1000", 10)) return reply(429, { error: "The document readers have reached their limit for this month. Please try again next month." }, origin);
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
          model: route.model(env),
          max_tokens: route.maxTokens,
          tools: [route.tool],
          tool_choice: { type: "tool", name: route.tool.name },
          messages: [{ role: "user", content: [file, { type: "text", text: route.prompt }] }]
        })
      });
    } catch {
      return reply(502, { error: "The reader couldn't be reached. Please try again later." }, origin);
    }
    if (!res.ok) return reply(502, { error: res.status === 400 || res.status === 413 ? "That file is too long or too large to read in one go. Try only the summary and conclusions pages." : "The reader couldn't read that file. Please try again later." }, origin);

    const out = await res.json();
    const use = (out.content || []).find(c => c.type === "tool_use" && c.name === route.tool.name);
    if (!use) return reply(502, { error: "The reader couldn't find what it needed in that file." }, origin);
    return reply(200, { kind, result: path === "/read" ? clean(use.input || {}) : cleanTo(route.tool, use.input || {}) }, origin);
  }
};

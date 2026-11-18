# Launch gates

Every change made because something is not yet in place is listed here, with the switch that undoes it. Kept off the public site by `_config.yml`.

## The switches (in `_config.yml`)

| Switch | Turn to `true` when | What it turns back on |
|---|---|---|
| `pi_cover` | Professional indemnity cover is bound and the certificate is in hand | Working-with page says cover is held. Together with `aml_supervised`, the CBAM advice products |
| `aml_supervised` | HMRC anti-money-laundering supervision is in place, or a professional adviser confirms in writing that it is not needed | Together with `pi_cover`, the CBAM advice products: the Readiness Review, short written answers, Importer Readiness, first return and the CBAM Desk subscription, with their buttons and prices across the site |
| `vat_registered` | HMRC confirms VAT registration | CBAM Desk terms read "All prices exclude VAT, which is charged at the prevailing rate" |

## How to flip one

1. Change the switch in `_config.yml` from `false` to `true`.
2. Run `python3 _scripts/launch_gates.py` from the repo root. It updates the pages that cannot read the switches (listed below) and warns if any price on them no longer matches `cbam-desk.md`.
3. Add a line to `WEBSITE-UPDATES.md`, open a pull request, merge.

To reverse, set the switch back to `false` and run the script again.

## What each switch controls

**Pages that read the switches directly (Liquid):** `index.html` (home slides), `services.md`, `cbam-desk.md` (booking note, VAT line), `cbam-desk/is-it-a-cbam-good.md`, `working-with.md` (PI line), `_posts/2026-11-11-twelve-dates-to-easter.md`, `_posts/2026-11-10-catholic-church-science-business-environment.md`.

**Pages flipped by the script** (registry: `_scripts/launch_gates_registry.json`, gate "advice"): `tools/uk-cbam-countdown.html`, `tools/dashboards/cbam-exposure-tracker.html`, `tools/dashboards/ni-regulatory-horizon.html` and its build script `_scripts/dashboards/horizon_build.py`, `blog/focus-on-metals-manufacturing-november-2026/index.html`.

**If prices change:** update the "open" text for each registry entry to the new price before flipping, or the script will warn.

## Not on the website (tracked on the master list)

- Public-sector tendering registrations (eTendersNI and Ireland's eTenders) wait for `pi_cover`.
- Paid ministerial contact for clients waits for the lobbying register once `vat_registered` is true.

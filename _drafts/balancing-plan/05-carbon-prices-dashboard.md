---
item: 5
title: "Carbon prices: UK ETS, EU ETS and the UK CBAM rate"
type: Dashboard (specification; build needs data pulls)
pillar: CBAM
audience: CBAM Desk clients, importers, energy-intensive manufacturers
status: DRAFT SPECIFICATION for panel review
verify:
  - Licence and reuse terms for ICE Endex and EEX auction results before publishing figures
sources:
  - UK ETS auction results (GOV.UK; auction platform to confirm: ICE Futures Europe, per Panel B)
  - EU ETS primary auction results (EEX)
  - HMRC, Rates for the CBAM (quarterly)
  - DESNZ/HMT statements on UK–EU ETS linking (target 2028)
---

## What it answers

1. What is the UK carbon price this week, and the EU price, and how wide is the gap?
2. What UK CBAM rate applies this quarter, and what would the next quarter's be if prices hold?
3. What does a tonne of steel, aluminium or fertiliser cost in CBAM at today's prices?

## Panels

| Panel | Data | Refresh |
| --- | --- | --- |
| UK ETS auction clearing price, 2021 to date | UK ETS auction results | after each auction |
| EU ETS auction price, same axis in £ (Bank of England daily rate) | EEX results | weekly |
| UK–EU price gap and what linking in 2028 would mean | computed | weekly |
| UK CBAM rate by quarter (published) | HMRC | quarterly |
| Cost per tonne of product at the current rate (steel, aluminium, ammonium nitrate, cement) using HMRC defaults | HMRC defaults × rate | quarterly |
| Dated events: auctions, rate publications, linking milestones | site's Regulatory Horizon | as they occur |

Every table downloadable as CSV, as on the other dashboards. Static build from a script in `_scripts/dashboards/`, refreshed by the Friday run.

**Build effort:** medium; two to three days once data access is confirmed.

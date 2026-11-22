---
item: 32
title: "Legislatures and committees monitor: Westminster, the devolved legislatures, the Oireachtas and the Crown Dependencies"
type: Dashboard (merge of three built 22 Nov)
pillar: Public affairs
status: DRAFT SPECIFICATION for panel review
inputs:
  - Artifact: UK Legislatures Committee Monitor (22 Nov 2026)
  - Artifact: Oireachtas Committee Monitor (22 Nov 2026)
  - Artifact: Crown Dependencies Legislatures Monitor (22 Nov 2026)
verify:
  - Each source's reuse terms (UK Parliament committees API/Open Parliament Licence; Oireachtas open data; States of Jersey, States of Guernsey, Tynwald)
  - Refresh method that fits a static site (weekly Friday rebuild)
---

## Design
One page, one filter bar: legislature, topic (environment, energy, trade, agriculture, planning, water, waste), status (open inquiry, evidence deadline, report published).
- **Open calls for evidence** first, sorted by deadline: the actionable list for clients and trade bodies.
- **This week's sittings** on the filtered topics.
- **Reports published** in the last 90 days, with the Government's response due date.
- Cross-links to the NI Consultations Monitor and the EU Law dashboard: together they cover "who is asking, by when".

**Why:** completes the public affairs toolset; already mostly built. **Effort:** low.

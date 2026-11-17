---
title: "CO₂e and global warming potential, in detail"
answer: "CO₂e (carbon dioxide equivalent) puts every greenhouse gas into one unit: tonnes of gas multiplied by its global warming potential (GWP). A GWP compares the heat one kilogram of a gas traps over a set period, usually 100 years, with one kilogram of CO₂. It depends on two things: how strongly the gas absorbs heat and how long it lasts. That is why a short-lived gas can have a tiny GWP however potent it is, and why the same gas has different GWPs over 20 and 100 years."
description: "CO₂e and GWP explained properly: how a GWP is calculated, strength and lifetime, GWP-20 against GWP-100, GWP*, natural and man-made gases, where Earth's carbon is stored, and whether methane and nitrous oxide can be captured or burned."
theme: "Carbon basics"
order: 13
level: "Intermediate"
read_time: "17-minute"
checked: 2026-11-17
---

Almost every carbon number you see, on a footprint, a CBAM declaration, a council report or a product label, is in **tonnes of CO₂e**. Most people know it means “carbon dioxide equivalent”. Fewer know what the equivalence actually is, why it changes depending on who you ask, or why a gas that vanishes in days can count for almost nothing while CO₂, the weakest of the lot per kilogram, is the one that matters most.

This page goes one level deeper than [Why is everything counted as “carbon”?]({{ '/learn/why-everything-is-carbon/' | relative_url }}).

## CO₂e in one line

**tonnes of CO₂e = tonnes of gas × GWP**

| Gas released | GWP-100 (AR5, used in UK reporting) | CO₂e |
|---|---|---|
| 1 tonne of CO₂ | 1 | 1 tonne |
| 1 tonne of methane | 28 | 28 tonnes |
| 1 tonne of nitrous oxide | 265 | 265 tonnes |
| 10 kg of HFC-134a refrigerant | 1,300 | 13 tonnes |
| 1 kg of SF₆ | 23,500 | 23.5 tonnes |

Add the right-hand column up and you have a carbon footprint. Everything interesting is hidden in the middle column.

## What a GWP actually is

The IPCC defines a GWP as the heat trapped by a one-off release of one kilogram of a gas, added up over a chosen period, divided by the heat trapped by one kilogram of CO₂ over the same period. In symbols:

**GWP(H) = ∫₀ᴴ forcing from 1 kg of gas dt ÷ ∫₀ᴴ forcing from 1 kg of CO₂ dt**

where *H* is the time horizon, usually 100 years. The top and bottom are each an area under a curve: how hard the gas pushes on the climate each year, times how many years it is there to push.

<figure class="learn-figure"><a href="{{ '/assets/learn/gwp-area-explained.svg' | relative_url }}" title="Open the diagram full size"><img src="{{ '/assets/learn/gwp-area-explained.svg' | relative_url }}" alt="Two panels. One kilogram of methane traps far more heat at first but most has gone within a few decades, so its curve is tall and short. One kilogram of CO2 traps much less heat but stays for centuries, so its curve is low and long. The GWP is the area under the gas curve divided by the area under the CO2 curve over the chosen period: about 28 for methane over 100 years and about 81 over 20 years." loading="lazy"></a><figcaption>A GWP is a ratio of two areas: strength times staying power. Tap or click to open it full size.</figcaption></figure>

So every GWP is built from two ingredients.

**1. Strength: how much heat each kilogram traps.** This is the gas's **radiative efficiency**. It depends on which infrared wavelengths the molecule absorbs and how much of that wavelength is already being absorbed by other gases (see the band chart on the [earlier page]({{ '/learn/why-everything-is-carbon/' | relative_url }})).

| Gas | Radiative efficiency (W m⁻² per ppb, IPCC AR6) | Compared with CO₂, per molecule |
|---|---|---|
| Carbon dioxide | 0.0000133 | 1 |
| Methane | 0.000388 | about 29 times |
| Nitrous oxide | 0.0032 | about 240 times |
| SF₆ | 0.567 | about 43,000 times |

CO₂ is weak per molecule partly because its main absorption bands are already close to saturated: there is so much of it that each extra molecule adds less than the one before. Gases that absorb in the clear “window” between 8 and 14 µm are strong because almost nothing else is absorbing there.

**2. Staying power: how long it lasts.** A molecule only traps heat while it is in the air.

<figure class="learn-figure"><a href="{{ '/assets/learn/gwp-decay-curves.svg' | relative_url }}" title="Open the chart full size"><img src="{{ '/assets/learn/gwp-decay-curves.svg' | relative_url }}" alt="Curves of the share of a one-off release still in the air over 100 years. HFO-1234yf, lifetime 12 days, vanishes almost at once. Methane, lifetime 11.8 years, is mostly gone within 30 to 40 years. Nitrous oxide, 109 years, falls to about 40%. Carbon dioxide drops quickly at first as oceans and plants take some up, then levels off: about 40% remains after 100 years and about a fifth lasts for millennia." loading="lazy"></a><figcaption>Methane is a sprinter; CO₂ never really leaves. Tap or click to open it full size.</figcaption></figure>

Most gases decay in a simple way: after one “lifetime” about 37% is left, after two about 14%, and so on. CO₂ is different. It is not destroyed in the air at all; it is shared out between the air, the oceans, plants and soils. The ocean and plants take up a large share within decades, but **around 40% is still there after a century, and about a fifth lasts for thousands of years**, until rocks slowly weather it away. That is why CO₂ has no single lifetime.

## Why some gases count for little and others for a lot

| Gas | Strength per kg | Lifetime | GWP-20 | GWP-100 |
|---|---|---|---|---|
| HFO-1234yf (car air conditioning) | Strong | 12 days | 1.81 | 0.501 |
| HFC-32 | Strong | 5.4 years | 2,690 | 771 |
| Methane | Strong | 11.8 years | 81.2 | 27.9 |
| HFC-134a | Strong | 14 years | 4,140 | 1,530 |
| Nitrous oxide | Strong | 109 years | 273 | 273 |
| SF₆ | Extreme | about 1,000 years | 18,200 | 24,300 |
| CF₄ | Strong | 50,000 years | 5,300 | 7,380 |
| CO₂ | Weak | Centuries to millennia | 1 | 1 |

(IPCC AR6 values.)

Three patterns explain almost everything:

- **Potent but gone in days means a tiny GWP.** HFO-1234yf absorbs heat strongly, molecule for molecule, but sunlight and the air's chemistry break it down in about 12 days. It has no time to do much: GWP-100 of 0.501, less than CO₂ itself. That is why it replaced HFC-134a (GWP-100 1,530) in car air conditioning. **No gas with a very large GWP disappears in days**; a short life always pulls the number down.
- **Potent and lasting a decade means the number depends on the horizon.** Methane traps about 81 times as much heat as CO₂ over its first 20 years but only about 28 times over 100, because by year 40 most of it has gone while the CO₂ is still there. Short-lived gases always look bigger on a 20-year view.
- **Potent and lasting centuries means a huge, stable number.** SF₆, CF₄ and nitrous oxide are still there at year 100, so their GWP-20 and GWP-100 are similar, and for the longest-lived ones the 100-year figure is higher.

**And CO₂?** It has the lowest GWP of all, exactly 1, by definition. But it is emitted in vast amounts and much of it stays for thousands of years, so it causes most of the warming. A low GWP does not mean a small problem.

<figure class="learn-figure"><a href="{{ '/assets/learn/gwp-20-vs-100.svg' | relative_url }}" title="Open the chart full size"><img src="{{ '/assets/learn/gwp-20-vs-100.svg' | relative_url }}" alt="IPCC AR6 values. HFO-1234yf, 12 days: 1.81 over 20 years, 0.501 over 100. Methane, 11.8 years: 81.2 and 27.9. HFC-32, 5.4 years: 2,690 and 771. HFC-134a, 14 years: 4,140 and 1,530. Nitrous oxide, 109 years: 273 and 273. CF4, 50,000 years: 5,300 and 7,380. SF6, 1,000 years: 18,200 and 24,300. Short-lived gases fall between 20 and 100 years; long-lived ones hold or rise." loading="lazy"></a><figcaption>The shorter the life, the bigger the gap between the two numbers. Tap or click to open it full size.</figcaption></figure>

## Natural or man-made, and where the carbon lives

Some greenhouse gases have always been in the air; others exist only because people make them.

<figure class="learn-figure"><a href="{{ '/assets/learn/ghg-natural-vs-added.svg' | relative_url }}" title="Open the chart full size"><img src="{{ '/assets/learn/ghg-natural-vs-added.svg' | relative_url }}" alt="Share of today's concentration that was there before industry: carbon dioxide about 65% (426.8 ppm in 2025, 153% of 1750); methane about 37% (1,948 ppb, 267% of 1750); nitrous oxide about 79% (339.1 ppb, 126% of 1750); CF4 about 41% (34 ppt natural background from rocks, 83 ppt in 2016); SF6, C2F6, NF3 and HFCs entirely man-made." loading="lazy"></a><figcaption>Nitrous oxide is mostly natural; SF₆ and the HFCs are entirely ours. Tap or click to open it full size.</figcaption></figure>

| Gas | Natural sources | Human sources | Concentration |
|---|---|---|---|
| Carbon dioxide | Breathing, rotting, volcanoes, the oceans | Burning fossil fuels, cement, clearing land | 426.8 ppm in 2025, 153% of the 1750 level (WMO) |
| Methane | Wetlands, termites, geological seeps | Cattle, landfill, rice, gas and coal | 1,948 ppb in 2025, 267% of 1750 (WMO) |
| Nitrous oxide | Soils and oceans (bacteria) | Fertiliser, manure, nitric acid plants | 339.1 ppb in 2025, 126% of 1750 (WMO) |
| CF₄ | A small, steady release from fluorite and granite in the Earth's crust | Aluminium smelting, electronics | 34 ppt before industry; 82.7 ppt by 2016 |
| SF₆ | None of significance | Electrical switchgear, magnesium | 12.2 ppt in 2025, up from 3.5 ppt in 1995 (WMO) |
| C₂F₆, NF₃, HFCs | None | Aluminium, electronics, refrigeration | Entirely man-made |

So **nitrous oxide is not a man-made gas**: about four-fifths of what is in the air today would be there anyway; people have added the rest. Methane is the opposite: nearly two-thirds of today's methane is our addition. And CF₄ is a curiosity: ice cores and old air show a natural background of about 34 parts per trillion, leaking from rocks, before aluminium smelters more than doubled it. SF₆, C₂F₆, NF₃ and the HFCs have no meaningful natural source at all.

**Where is all the carbon?** The answer puts the atmosphere in its place.

<figure class="learn-figure"><a href="{{ '/assets/learn/earth-carbon-reservoirs.svg' | relative_url }}" title="Open the chart full size"><img src="{{ '/assets/learn/earth-carbon-reservoirs.svg' | relative_url }}" alt="Billions of tonnes of carbon on a log scale: atmosphere about 900; land plants about 450; soils in the top metre 1,500 to 2,400; permafrost region 1,300 to 1,600; oceans about 38,000; everything above the surface about 43,500, or 0.2% of the total; crust, mantle and core about 1.85 billion, or 99.8%. The air holds about 0.00005% of Earth's carbon." loading="lazy"></a><figcaption>The air is a thin film on a planet made of carbon-rich rock. Tap or click to open it full size.</figcaption></figure>

| Store | Carbon (billion tonnes) | Share |
|---|---|---|
| Atmosphere | about 900 | about 0.00005% of Earth's total |
| Land plants | about 450 | |
| Soils (top metre) | 1,500–2,400 | |
| Permafrost region | 1,300–1,600 | |
| Oceans | about 38,000 | |
| **Everything above the surface** | **about 43,500** | **0.2%** |
| **Crust, mantle and core** | **about 1.85 billion** | **99.8%** |

The Deep Carbon Observatory, a ten-year international study reported in 2019, estimated that 99.8% of Earth's carbon is underground, in the crust, mantle and core, though the deep figures are uncertain. Most of that is locked away for geological time. It reaches the air mainly through volcanoes, which the US Geological Survey estimates release about 0.18–0.44 billion tonnes of CO₂ a year, **roughly a hundredth of what people now emit**.

The point is not that the air's share is small. It is that the air is a **thin, sensitive film**: moving even a sliver of the crust's carbon (coal, oil and gas) into it in two centuries has raised CO₂ by half. The deep Earth recycles carbon over millions of years; we are doing it in a lifetime.

## Which number is “right”?

None of them; each answers a different question.

| Metric | The question it answers | Who uses it |
|---|---|---|
| **GWP-100** | How much heat does a tonne trap over a century, compared with CO₂? | UK and NI inventories, DESNZ conversion factors, the Paris Agreement rulebook, most corporate reporting |
| **GWP-20** | How much over the next 20 years? | Used to highlight short-term warming, especially methane |
| **GTP** (global temperature change potential) | How much warmer would it be at a given future year? | IPCC reports; rarely used in rules |
| **GWP*** (“GWP-star”) | How much warming does a *change* in a short-lived gas's emission rate cause? | Proposed by Oxford researchers; debated, not used in official inventories |

**GWP\*** deserves a word because it comes up in farming debates. Its authors at Oxford point out that methane is broken down within decades, so **a steady rate of methane emissions keeps the methane in the air roughly constant and adds little new warming**, while a steady rate of CO₂ emissions keeps adding warming every year because CO₂ accumulates. GWP* therefore counts a *rise* in methane emissions heavily and a *fall* as a cooling. Supporters say this matches the physics of temperature better. Critics argue it can favour those who were already high emitters, because standing still counts as nothing. It is a live debate; for now every official UK inventory uses GWP-100.

**Which vintage?** The IPCC has revised its GWPs in each assessment. UK and NI reporting, and the DESNZ conversion factors for 2025 and 2026, use **AR5** (methane 28, nitrous oxide 265). The latest set is **AR6** (methane 27.9, or 29.8 for fossil methane and 27.0 for non-fossil, because fossil methane leaves extra CO₂ behind when it breaks down; nitrous oxide 273). Check which set a figure uses before comparing it with another. (Checked 17 November 2026.)

### Think of a firework and a candle

| Light show | Greenhouse gases |
|---|---|
| A firework: dazzling, over in seconds | HFO-1234yf: potent, gone in days |
| A flare: bright for a few minutes | Methane: potent, mostly gone in decades |
| A candle: dim, but burns all night | CO₂: weak, but lasts centuries |
| Asking “how much light in the first minute?” | GWP-20: favours the flare |
| Asking “how much light over the whole evening?” | GWP-100: the candle catches up |
| Lighting a new flare every minute | Steady methane emissions: a constant glow, not a growing one (the GWP* argument) |
| Lighting a new candle every minute | Steady CO₂ emissions: the room keeps getting brighter |

## Can we capture other gases, or burn them?

Capture is usually talked about only for CO₂ (see [Carbon capture and carbon negative]({{ '/learn/carbon-capture-and-carbon-negative/' | relative_url }})). The other gases have their own answers, and for methane the best answer is often to **burn it**.

<figure class="learn-figure"><a href="{{ '/assets/learn/capture-by-gas.svg' | relative_url }}" title="Open the diagram full size"><img src="{{ '/assets/learn/capture-by-gas.svg' | relative_url }}" alt="Four columns. Carbon dioxide: captured from chimneys (CCS) or the air (DACCS) and stored or used; plants and soils too. Methane: collected from landfill, digesters, slurry stores and coal mines and burned for energy or flared; feed additives cut cow methane. Nitrous oxide: in factories, catalysts split it into nitrogen and oxygen; on fields there is no capture, only inhibitors and using less nitrogen. F-gases: recovered from equipment at service and end of life, then reclaimed, reused or destroyed at high temperature." loading="lazy"></a><figcaption>Only CO₂ is captured and stored; the rest are collected, burned or destroyed. Tap or click to open it full size.</figcaption></figure>

### Methane: collect it and burn it

Methane is natural gas. Where it comes out of a point source (a landfill, a slurry store, an anaerobic digester, a coal mine, a leaking well), it can be collected and burned:

**CH₄ + 2O₂ → CO₂ + 2H₂O**

Sixteen grams of methane become 44 grams of CO₂, so **one tonne of methane becomes 2.75 tonnes of CO₂**. On a GWP-100 of 28, that turns 28 tonnes of CO₂e into 2.75: a cut of about 90%. If the methane is **biogenic** (from rotting waste, slurry or crops), inventories treat the resulting CO₂ as part of the natural carbon cycle and count it as zero, so the cut is close to 100%. Better still is to **use** it: burned in an engine or boiler, it replaces fossil fuel that would otherwise have been burned.

<figure class="learn-figure"><a href="{{ '/assets/learn/methane-vent-flare-use.svg' | relative_url }}" title="Open the diagram full size"><img src="{{ '/assets/learn/methane-vent-flare-use.svg' | relative_url }}" alt="One tonne of methane vented to the air counts as 28 tonnes of CO2 equivalent (GWP-100, AR5). Flared, it burns to 2.75 tonnes of CO2, about 90% less warming. Burned for heat or power, it gives the same 2.75 tonnes but replaces fossil fuel that would otherwise be burned. If the methane is biogenic, inventories count the CO2 as zero. Flares are not perfect and some methane slips through." loading="lazy"></a><figcaption>A flare is a crude fix; a digester or engine is a better one. Tap or click to open it full size.</figcaption></figure>

Flares are not perfect: some methane slips through unburned. That is why the EU Methane Regulation, (EU) 2024/1787, in force since 4 August 2024, banned routine venting and flaring in the EU oil and gas sector from 5 February 2026 (with exceptions for emergencies and where unavoidable) and set efficiency requirements for the flares that remain.

**Diffuse methane is harder.** Most farm methane comes from cows' digestion, breathed out across a whole field. It cannot be piped to a flare. The options there are to make less: the feed additive 3-NOP (sold as Bovaer) cuts methane from dairy cows by about 30% in studies, and was assessed as safe by the Food Standards Agency and Food Standards Scotland in March 2023. Taking methane back out of the open air, “methane removal”, is still at the research stage.

### Nitrous oxide: split it, or do not make it

In factories, nitrous oxide comes out of a chimney, so it can be destroyed. At nitric acid plants (the step that turns ammonia into fertiliser), catalysts placed in or after the ammonia burner split it back into nitrogen and oxygen:

**2N₂O → 2N₂ + O₂**

Manufacturers report cuts of up to about 90% from catalysts inside the burner and up to about 99% from catalysts treating the tail gas, at low cost per tonne of CO₂e. That is why European fertiliser has a much lower footprint than fertiliser from plants without abatement (see [Fertiliser and the nitrogen cycle]({{ '/learn/fertiliser-and-the-nitrogen-cycle/' | relative_url }})).

On fields, nitrous oxide seeps out of soil over whole farms; there is nothing to capture. The answers are to apply less nitrogen, at the right time, in the right form, and to use nitrification inhibitors that slow the soil bacteria that make it.

### F-gases: recover and destroy

Refrigerants and SF₆ sit inside equipment, so the job is to stop leaks, recover the gas at service and end of life, and reclaim or destroy it at high temperature. Northern Ireland follows the EU F-gas Regulation, (EU) 2024/573, which requires this; Great Britain has its own rules.

## Why it matters in Northern Ireland

- **NI's footprint is unusually non-CO₂.** In 2024, methane was 29.5% and nitrous oxide 8.0% of NI's emissions (DAERA and NISRA). The choice of metric moves NI's numbers more than most of the UK's: on GWP-20, the methane share would nearly triple.
- **The GWP\* debate is a farming debate.** Because NI agriculture is methane-heavy, how methane is counted affects how farm progress looks. Official NI inventories and carbon budgets under the Climate Change Act (Northern Ireland) 2022 use GWP-100 (AR5).
- **Methane is capturable here.** Landfill sites, anaerobic digesters and slurry stores are point sources; covering slurry stores and feeding digesters turns an emission into a fuel.
- **CBAM counts nitrous oxide.** Both CBAMs count nitrous oxide in the embedded emissions of fertiliser, in CO₂e, so a supplier's catalyst decides part of the bill.

## Examples

<div class="example" markdown="1">
<p class="sector">Agriculture and food</p>

### A dairy farm with a slurry store

A 200-cow dairy farm stores slurry in an open lagoon. The slurry gives off methane.

| Option | What happens to the methane |
|---|---|
| Open store | Vented: counted at GWP 28 |
| Cover the store and flare the gas | Burned to CO₂; biogenic, so counted as close to zero |
| Send slurry to an anaerobic digester | Burned for heat and power, replacing fossil fuel |
| Feed 3-NOP to the herd | About 30% less methane from the cows themselves (studies) |

**The lesson:** slurry methane is a point source you can catch; cow breath is not. Tackle the store first. The figures here are illustrative; a farm-level assessment needs measured data.
</div>

<div class="example" markdown="1">
<p class="sector">Manufacturing</p>

### A firm replacing its chiller refrigerant

A food factory's chiller holds 50 kg of HFC-134a and loses about 10% a year.

| | HFC-134a | HFO-1234yf (or similar low-GWP option) |
|---|---|---|
| Annual leak | 5 kg | 5 kg |
| GWP-100 | 1,300 (AR5) | under 1 |
| CO₂e | 6.5 tonnes | under 0.005 tonnes |

**The lesson:** the same leak, nearly 1,300 times smaller in CO₂e, because the new gas lasts days, not years. Check safety, flammability and the PFAS question before switching: some HFOs fall within broad PFAS definitions and break down to persistent trifluoroacetic acid, an issue under active review.
</div>

<div class="example" markdown="1">
<p class="sector">Public sector</p>

### A council's closed landfill

A council owns a closed landfill still producing gas.

**What to check:** whether the gas is collected and flared or used for power; flare efficiency; and how much escapes through the cap. Every tonne of methane captured and burned cuts about 90% of its warming effect, and more if the energy is used.

**The lesson:** for most councils, landfill methane is the single biggest emission they can still do something about at source.
</div>

## Common mistakes

1. **“CO₂e means CO₂.”** It is all seven gases, converted.
2. **“A low GWP means a harmless gas.”** CO₂ has the lowest GWP of all and causes most of the warming.
3. **“A short-lived gas can have a huge GWP.”** A short life always pulls the number down; potency alone is not enough.
4. **“GWP-20 is the true number.”** It answers a different question. Say which you used.
5. **“Burning methane is just more emissions.”** It cuts warming by about 90%, and more if the methane is biogenic or the energy is used.
6. **“We can capture nitrous oxide from fields.”** Only from chimneys; on fields, the answer is making less.

Previous: [Why is everything counted as “carbon”?]({{ '/learn/why-everything-is-carbon/' | relative_url }}) · Related: [Carbon capture and carbon negative]({{ '/learn/carbon-capture-and-carbon-negative/' | relative_url }}) · [Fertiliser and the nitrogen cycle]({{ '/learn/fertiliser-and-the-nitrogen-cycle/' | relative_url }})

## Sources

Checked 17 November 2026.

- **GWPs, lifetimes and radiative efficiencies:** IPCC, [AR6 WG1 Chapter 7 Supplementary Material, Table 7.SM.7](https://www.ipcc.ch/report/ar6/wg1/downloads/report/IPCC_AR6_WGI_Chapter07_SM.pdf) (2021) · HFO-1234yf values (12 days; GWP-20 1.81; GWP-100 0.501) as tabulated from AR6 by [UNEP and ASHRAE via Project Drawdown](https://drawdown.org/explorer/deploy-alternative-refrigerants/figure-a1) and [Fluorocarbons.org](https://www.fluorocarbons.org/wp-content/uploads/2020/10/Fluorocarbon-Molecules-environmental-properties-and-main-applications-2021-September-FINAL.pdf) (industry body) · GHG Protocol, [Global Warming Potential Values (August 2024)](https://ghgprotocol.org/sites/default/files/2024-08/Global-Warming-Potential-Values%20%28August%202024%29.pdf) (AR5 and fossil/non-fossil methane; secondary).
- **Concentrations and natural shares:** WMO, [Greenhouse Gas Bulletin No. 22](https://www.justsecurity.org/wp-content/uploads/2026/10/WMO-GHG-22.pdf) (October 2026; 2025 values and shares of 1750; via a third-party copy) and [WMO news release](https://wmo.int/node/39151) · NOAA Global Monitoring Laboratory, [AGGI](https://gml.noaa.gov/aggi/aggi.html) · Trudinger et al. 2016, *Atmos. Chem. Phys.* 16, 11733 (CF₄ natural background 34.1 ppt; C₂F₆ none) · AGAGE (CF₄ 82.7 ppt in 2016, as cited by [Mühle et al.](https://acp.copernicus.org/preprints/acp-2020-937/acp-2020-937.pdf)). The natural and added shares are my arithmetic.
- **Carbon stores:** Deep Carbon Observatory findings published in *Elements*, October 2019 (via [EurekAlert](https://www.eurekalert.org/news-releases/736161) and [Eos](https://eos.org/?p=134727)) · IPCC AR6 WG1 [Figure 5.12](https://www.ipcc.ch/report/ar6/wg1/figures/chapter-5/figure-5-12) (ocean, land and atmosphere stocks; ranges as commonly summarised) · NOAA Arctic Report Card 2024 (permafrost) · USGS volcanic CO₂ estimate 180–440 million tonnes a year (as quoted by [Gigafact](https://gigafact.org/fact-briefs/do-volcanoes-emit-more-co2-than-humans); USGS page not opened). The 0.00005% figure is my arithmetic.
- **CO₂ decay curve:** the impulse-response fit of Joos et al. (2013) used by IPCC AR5; drawn here for illustration.
- **UK and NI basis:** DESNZ, [GHG conversion factors 2026 methodology](https://assets.publishing.service.gov.uk/media/6a2940543b15d05a7ce3202e/2026-GHG-conversion-factors-methodology-report.pdf) · DAERA and NISRA, [NI GHG inventory 1990–2024](https://datavis.nisra.gov.uk/daera/northern-ireland-greenhouse-gas-inventory-1990-2024-statistical-bulletin.html) (9 June 2026).
- **GWP\*:** Lynch, Cain, Pierrehumbert and Allen 2020, [*Environmental Research Letters*](https://www.leap.ox.ac.uk/node/1051686), doi:10.1088/1748-9326/ab6d7e · Cain, [Carbon Brief guest post](https://www.carbonbrief.org/guest-post-a-new-way-to-assess-global-warming-potential-of-short-lived-pollutants) (7 June 2018). The critics' argument is summarised from the wider debate and not checked against a single source.
- **Methane:** Regulation (EU) 2024/1787, in force 4 August 2024; routine venting and flaring ban from 5 February 2026 (as summarised by [White & Case](https://whitecase.com/insight-alert/are-you-ready-new-eu-rules-methane-emissions-energy-sector) and [Conventus Law](https://conventuslaw.com/?p=121809); EUR-Lex not reachable today) · Food Standards Agency, [3-NOP (Bovaer 10) authorisation background](https://www.food.gov.uk/our-work/annex-m-rp1059-3-nitrooxypropanol-as-a-feed-additive-for-ruminants-for-milk-production-and-for-reproduction) (safety assessment published 31 March 2023) · Ohio State University, [3-NOP meta-analyses](https://dairy.osu.edu/newsletter/buckeye-dairy-news/volume-26-issue-3/3-nop-bovaer%E2%84%A2-receives-fda-approval) (about 28–33% less enteric methane).
- **Nitrous oxide abatement:** International Platinum Group Metals Association, [N₂O abatement](https://ipa-news.com/index/about-pgms/pgm-uses/pollution-control/n2o-abatement.html) (secondary catalysts up to 90%) · Topsoe, [tertiary catalyst](https://topsoe.com/hubfs/CAMPAIGNS/TertiNOx/TertiNOx%20details.pdf?hsLang=en) (up to 99%; manufacturer claim) · Nitric Acid Climate Action Group, nitrous oxide from nitric acid production (abatement cost).
- **F-gases in NI:** see [Why is everything counted as “carbon”?]({{ '/learn/why-everything-is-carbon/' | relative_url }}).
- **Not checked against a primary source:** the saturation explanation for CO₂'s low radiative efficiency (standard physics); that methane removal from open air is at the research stage; the PFAS and trifluoroacetic acid point on HFOs (under review by regulators). Per-molecule ratios are my arithmetic from the IPCC radiative efficiencies. The examples are illustrative.

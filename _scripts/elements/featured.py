"""The eight featured elements: full context, safety panel (COSHH, exposure limits,
UN numbers, hazards of the element itself) and the compounds people meet in nature,
manufacturing and the climate system. Checked 21 November 2026.

Conventions
- Classification: harmonised entries in CLP Annex VI (EU CLP applies in Northern
  Ireland under the Windsor Framework; GB CLP and the GB mandatory classification
  list apply in Great Britain). Where no harmonised entry exists, it says so.
- WEL = workplace exposure limit from HSE EH40/2005 (4th edition, January 2020),
  approved for use in Northern Ireland by HSENI. LTEL = 8-hour, STEL = 15-minute.
- UN numbers and classes from the UN Model Regulations / ADR.
- Anything marked "check" has not been re-read against the primary table for this
  draft and must be confirmed before publication.
"""

CHECKED = "21 November 2026"

F = {}

F['P'] = dict(
 post='/blog/2026/11/phosphorus-the-nutrient-that-fed-the-farms-and-fouled-the-lough/',
 pdf='/assets/briefings/elements/phosphorus-briefing.pdf',
 env="Phosphorus is the nutrient that limits plant and algal growth in most fresh water. Too much of it, washed or leached from farmland, slurry and sewage, feeds the algal blooms that have covered Lough Neagh. DAERA describes excess phosphorus as the main cause of poor water quality in Northern Ireland.",
 eng="Mined phosphate rock is turned into fertiliser with sulfuric acid, making phosphoric acid and phosphogypsum waste. Phosphorus is also recovered from wastewater as struvite, and lithium iron phosphate (LFP) is now a leading battery chemistry.",
 geo="Phosphorus is not found free in nature. It is mined as phosphate rock (apatite), much of it from Morocco and Western Sahara. Phosphate rock carries cadmium, uranium and fluoride as impurities. Phosphorus is on the UK 2024 critical minerals list.",
 chem="Group 15, period 3. White phosphorus is a waxy solid that catches fire on its own in air and is very toxic; red phosphorus is stable and is used on match strikers. In soils and water it is almost always present as phosphate (PO₄³⁻), which binds tightly to iron, aluminium and calcium.",
 land="Northern Ireland's farm system brings in more phosphorus, in feed and fertiliser, than it sends out in food. The surplus builds up in soil. The Soil Nutrient Health Scheme has found many fields above the agronomic target index. Fields above the target need no more phosphorus for years, and run-off from them reaches streams.",
 safety=dict(
  coshh="COSHH applies to phosphorus and its compounds. White phosphorus is one of the most dangerous elements to handle; it is not something a farm or general workshop should ever hold.",
  classes=[
   ("White (yellow) phosphorus", "Pyr. Sol. 1 H250 (catches fire spontaneously in air); Acute Tox. 2 H300 + H330 (fatal if swallowed or inhaled); Skin Corr. 1A H314; Aquatic Acute 1 H400. Harmonised (CLP Annex VI)."),
   ("Red phosphorus", "Flam. Sol. 1 H228 (flammable solid); Aquatic Chronic 3 H412. Harmonised (CLP Annex VI)."),
  ],
  wels=[
   ("Phosphine", "0.1 ppm LTEL; 0.2 ppm STEL (check)"),
   ("Orthophosphoric acid", "1 mg/m³ LTEL; 2 mg/m³ STEL (check)"),
   ("Yellow phosphorus", "0.1 mg/m³ LTEL; 0.3 mg/m³ STEL (check)"),
  ],
  un=[
   ("UN1381", "Phosphorus, white or yellow, dry or under water or in solution", "4.2 (6.1)"),
   ("UN2447", "Phosphorus, white, molten", "4.2 (6.1)"),
   ("UN1338", "Phosphorus, amorphous (red phosphorus)", "4.1"),
   ("UN1805", "Phosphoric acid, solution", "8"),
   ("UN2199", "Phosphine", "2.3 (2.1)"),
  ],
  risks="White phosphorus ignites in air at around 30 °C, burns deep into skin and is fatal in small doses; it is kept under water. Red phosphorus is far safer but burns easily and can release phosphine if contaminated. Phosphate fertilisers themselves are low hazard to people; the harm is to water.",
 ),
 compounds=dict(
  nature=[("Apatite (calcium phosphate)", "the mineral in phosphate rock, bones and teeth"),
          ("Orthophosphate (PO₄³⁻)", "the form plants take up and the form that feeds algae"),
          ("Organic phosphorus", "in manure, soil organic matter, DNA and ATP")],
  manufacturing=[("Phosphoric acid (H₃PO₄)", "made from rock and sulfuric acid; fertilisers, food, metal treatment"),
                 ("MAP, DAP and triple superphosphate", "the main phosphate fertilisers"),
                 ("Struvite (MgNH₄PO₄·6H₂O)", "recovered from wastewater and digestate as a slow-release fertiliser"),
                 ("Lithium iron phosphate (LiFePO₄)", "battery cathode material"),
                 ("Organophosphates", "pesticides such as glyphosate and historic sheep dips"),
                 ("Aluminium phosphide", "grain fumigant that releases toxic phosphine gas (UN1397)")],
  climate=[("No phosphorus greenhouse gas", "phosphorus acts on climate indirectly"),
           ("Algal blooms", "nutrient-rich lakes emit more methane"),
           ("Fertiliser manufacture", "energy for mining, acid production and transport")],
 ),
)

F['N'] = dict(
 post='/blog/2026/11/nitrogen-from-the-air-through-the-cow-into-the-lough-and-the-sky/',
 pdf='/assets/briefings/elements/nitrogen-briefing.pdf',
 env="Nitrogen gas is harmless, but reactive nitrogen is not. Ammonia from slurry and fertiliser damages peat bogs, woodland and lichens; nitrate leaches into water; nitrous oxide is a powerful greenhouse gas; and nitrogen oxides from engines harm lungs. DAERA reports that 97% of Northern Ireland's ammonia comes from agriculture.",
 eng="The Haber–Bosch process turns nitrogen from air and hydrogen from natural gas into ammonia, which becomes most of the world's fertiliser. It is energy intensive; fertilisers are covered by EU CBAM and will be covered by UK CBAM. Ammonia is also proposed as a shipping fuel and hydrogen carrier.",
 geo="Most of the Earth's nitrogen is in the atmosphere as N₂. Rocks hold little. Natural nitrate deposits exist in deserts such as Chile's Atacama.",
 chem="Group 15, period 2. The triple bond in N₂ makes it very unreactive, which is why fixing nitrogen takes either lightning, bacteria in clover roots, or an industrial plant. Reactive forms include ammonia (NH₃), ammonium (NH₄⁺), nitrate (NO₃⁻), nitrous oxide (N₂O) and nitrogen oxides (NOₓ).",
 land="Grassland in Northern Ireland runs on nitrogen from slurry, fertiliser and clover. The Nutrients Action Programme limits how much manure nitrogen can be applied and when. Ammonia drifts from farms onto designated sites, which is why planning applications for livestock housing are assessed for ammonia.",
 safety=dict(
  coshh="Nitrogen gas is not toxic, but it is a simple asphyxiant: in a confined space it displaces oxygen without warning. COSHH applies to the nitrogen compounds below, and confined-space rules apply to nitrogen gas.",
  classes=[
   ("Nitrogen, compressed gas", "Press. Gas H280 (contains gas under pressure; may explode if heated). No harmonised CLP entry; this is the supplier classification."),
   ("Nitrogen, refrigerated liquid", "Press. Gas H281 (contains refrigerated gas; may cause cryogenic burns)."),
  ],
  wels=[
   ("Nitrogen", "No WEL: an asphyxiant. Control is by keeping oxygen above safe levels."),
   ("Ammonia, anhydrous", "25 ppm LTEL; 35 ppm STEL"),
   ("Nitrogen dioxide", "0.5 ppm LTEL; 1 ppm STEL (from 2018)"),
   ("Nitrogen monoxide", "2 ppm LTEL (from 2018; check)"),
   ("Nitrous oxide", "100 ppm LTEL (check)"),
  ],
  un=[
   ("UN1066", "Nitrogen, compressed", "2.2"),
   ("UN1977", "Nitrogen, refrigerated liquid", "2.2"),
   ("UN1005", "Ammonia, anhydrous", "2.3 (8)"),
   ("UN1942", "Ammonium nitrate (≤0.2% combustible)", "5.1"),
   ("UN2067", "Ammonium nitrate based fertiliser", "5.1"),
   ("UN1070", "Nitrous oxide", "2.2 (5.1)"),
   ("UN2031", "Nitric acid", "8 (5.1 above certain strengths)"),
  ],
  risks="Nitrogen gas causes asphyxiation in tanks, silos and cold rooms; liquid nitrogen causes cold burns and expands about 700 times as it boils. Ammonium nitrate fertiliser is an oxidiser and must be stored away from fuel and organic matter.",
 ),
 compounds=dict(
  nature=[("Dinitrogen (N₂)", "78% of air"), ("Ammonium and nitrate", "plant-available nitrogen in soil"),
          ("Organic nitrogen", "proteins in grass, manure and soil organic matter")],
  manufacturing=[("Ammonia (NH₃)", "made by Haber–Bosch; the root of nearly all nitrogen fertiliser"),
                 ("Urea and protected urea", "solid fertiliser; protected urea cuts ammonia loss"),
                 ("Ammonium nitrate and calcium ammonium nitrate (CAN)", "the main straight nitrogen fertilisers in the UK and Ireland"),
                 ("Nitric acid (HNO₃)", "made from ammonia; its production emits nitrous oxide"),
                 ("Adipic acid and nylon", "another industrial source of nitrous oxide")],
  climate=[("Nitrous oxide (N₂O)", "a greenhouse gas with a 100-year global warming potential of 265 (AR5, as used in the UK inventory)"),
           ("Ammonia", "not a greenhouse gas, but it re-deposits and part of it is later emitted as N₂O"),
           ("Nitrogen oxides (NOₓ)", "form ground-level ozone, itself a greenhouse gas")],
 ),
)

F['S'] = dict(
 post='/blog/2026/11/sulfur-acid-rains-ingredient-now-a-fertiliser-we-buy/',
 pdf='/assets/briefings/elements/sulfur-briefing.pdf',
 env="Sulfur dioxide from coal and oil caused acid rain and smog. UK emissions fell by 98% between 1970 and 2022, mainly because coal use in power stations ended. Sulfate particles in the air reflect sunlight and cool the climate, so cleaner air has removed some masking of warming. Hydrogen sulfide from slurry is the gas that kills farmers.",
 eng="Most sulfur now comes from cleaning oil and gas, not mining. It is turned into sulfuric acid, the most produced industrial chemical, used for fertilisers, batteries and metal processing. Sulfur hexafluoride (SF₆), an insulating gas in electrical switchgear, is the most potent greenhouse gas regulated under the UNFCCC.",
 geo="Sulfur occurs as native sulfur near volcanoes, as sulfides such as pyrite (fool's gold) and galena, and as sulfates such as gypsum. Pyrite exposed to air and water makes acid mine drainage.",
 chem="Group 16, period 3. Spelled 'sulfur' by IUPAC and the Royal Society of Chemistry; 'sulphur' remains common in UK law and HSE guidance. Oxidation states run from −2 (sulfide, H₂S) to +6 (sulfate, sulfuric acid).",
 land="With less sulfur falling in rain, many crops and grass silage now need sulfur fertiliser. Sulfur is one of the nutrients reported under Northern Ireland's Soil Nutrient Health Scheme. Gypsum and other sulfates in soil, plasterboard waste and landfill can produce hydrogen sulfide.",
 safety=dict(
  coshh="COSHH applies to sulfur and its compounds. On farms, the controlling risk is hydrogen sulfide from slurry: HSENI warns that one breath at high concentration can kill.",
  classes=[
   ("Sulfur (element)", "Skin Irrit. 2 H315 (causes skin irritation). Harmonised (CLP Annex VI). Sulfur dust is also combustible and can explode."),
  ],
  wels=[
   ("Sulfur", "No specific WEL; general dust limits apply (10 mg/m³ inhalable, 4 mg/m³ respirable)"),
   ("Hydrogen sulfide", "5 ppm LTEL; 10 ppm STEL"),
   ("Sulfur dioxide", "0.5 ppm LTEL; 1 ppm STEL (from 2018)"),
   ("Sulfuric acid (mist)", "0.05 mg/m³ LTEL, thoracic fraction (check)"),
   ("Sulfur hexafluoride", "1,000 ppm LTEL (check)"),
  ],
  un=[
   ("UN1350", "Sulphur (some formed sulphur such as prills or granules may be exempt; check ADR special provision 242)", "4.1"),
   ("UN2448", "Sulphur, molten", "4.1"),
   ("UN1053", "Hydrogen sulphide", "2.3 (2.1)"),
   ("UN1079", "Sulphur dioxide", "2.3 (8)"),
   ("UN1830", "Sulphuric acid", "8"),
   ("UN1080", "Sulphur hexafluoride", "2.2"),
  ],
  risks="Solid sulfur is low in toxicity but burns with a blue flame to give choking sulfur dioxide, and its dust can explode. Molten sulfur releases hydrogen sulfide. Hydrogen sulfide deadens the sense of smell at high concentration, so the 'rotten eggs' warning disappears just when it matters.",
 ),
 compounds=dict(
  nature=[("Hydrogen sulfide (H₂S)", "from slurry, bogs, sewers and volcanoes"),
          ("Dimethyl sulfide (DMS)", "released by marine plankton; seeds clouds over the sea"),
          ("Pyrite (FeS₂) and gypsum (CaSO₄·2H₂O)", "common sulfur minerals"),
          ("Sulfate (SO₄²⁻)", "the form plants take up")],
  manufacturing=[("Sulfuric acid (H₂SO₄)", "fertiliser production, batteries, metal pickling"),
                 ("Ammonium sulfate and sulfur-containing fertilisers", "supply sulfur to grass and crops"),
                 ("Gypsum and plasterboard", "building material; must be kept separate from biodegradable waste in landfill"),
                 ("Sulfur hexafluoride (SF₆)", "insulating gas in electrical switchgear")],
  climate=[("Sulfate aerosols", "cool the climate by reflecting sunlight; their decline has unmasked some warming"),
           ("Sulfur hexafluoride (SF₆)", "100-year global warming potential of 23,500 (AR5) and a lifetime of thousands of years"),
           ("Shipping fuel", "the global 0.50% sulfur cap from 2020 cut ship SO₂ and some cooling with it")],
 ),
)

F['F'] = dict(
 post='/blog/2026/11/fluorine-in-your-fridge-your-frying-pan-and-your-teeth/',
 pdf='/assets/briefings/elements/fluorine-briefing.pdf',
 env="Fluorine's carbon compounds are the problem: hydrofluorocarbons (HFCs) and other F-gases are powerful greenhouse gases, and PFAS ('forever chemicals') persist in water, soil and blood. Fluoride also enters soils as an impurity in phosphate fertiliser.",
 eng="Fluorspar (calcium fluoride) is turned into hydrogen fluoride, the starting point for refrigerants, PTFE, lithium battery salts, uranium enrichment and aluminium smelting. Northern Ireland follows the EU F-gas Regulation (EU) 2024/573 under the Windsor Framework; Great Britain still applies its retained 2014-based regime.",
 geo="Fluorine occurs as fluorspar (fluorite), in cryolite and in fluoroapatite, the main mineral of phosphate rock. Natural fluoride in groundwater varies with geology.",
 chem="Group 17, period 2. The most electronegative and most reactive element; it reacts with almost everything, including glass. The carbon–fluorine bond is the strongest single bond in organic chemistry, which is why PFAS do not break down.",
 land="Northern Ireland's public water supply is not artificially fluoridated (NI Water, January 2025); Ireland's has been since 1964. Land contaminated by firefighting foam at airports, fire-training grounds and some industrial sites is the main PFAS land issue.",
 safety=dict(
  coshh="COSHH applies. Fluorine gas and hydrogen fluoride are among the most hazardous industrial chemicals; hydrofluoric acid burns may not hurt at first but can be fatal. Anyone handling them needs specific first aid (calcium gluconate) on site.",
  classes=[
   ("Fluorine (gas)", "Ox. Gas 1 H270 (may cause or intensify fire); Press. Gas H280; Acute Tox. 2 H330 (fatal if inhaled); Skin Corr. 1A H314. Harmonised (CLP Annex VI)."),
  ],
  wels=[
   ("Fluorine", "Listed in EH40 (check value before use)"),
   ("Hydrogen fluoride (as F)", "1.8 ppm LTEL; 3 ppm STEL"),
   ("Fluorides (as F)", "2.5 mg/m³ LTEL (check)"),
  ],
  un=[
   ("UN1045", "Fluorine, compressed", "2.3 (5.1, 8)"),
   ("UN1052", "Hydrogen fluoride, anhydrous", "8 (6.1)"),
   ("UN1790", "Hydrofluoric acid", "8 (6.1)"),
   ("UN1778", "Fluorosilicic acid", "8"),
   ("UN3159", "1,1,1,2-Tetrafluoroethane (R-134a)", "2.2"),
   ("UN3163", "Liquefied gas, n.o.s. (e.g. R-410A blends)", "2.2"),
  ],
  risks="Elemental fluorine is a pale yellow gas that is toxic, corrosive and ignites many materials on contact. It is handled only in specialist plant. Refrigerant gases are not toxic in normal use but displace oxygen in enclosed spaces and some are flammable (for example R-32 and the hydrocarbon alternatives).",
 ),
 compounds=dict(
  nature=[("Fluorite / fluorspar (CaF₂)", "the main ore"), ("Fluoroapatite", "in phosphate rock; carries fluoride into fertilisers"),
          ("Fluoride ion (F⁻)", "in groundwater, tea and toothpaste")],
  manufacturing=[("Hydrogen fluoride (HF)", "feedstock for almost all fluorochemicals"),
                 ("HFC refrigerants (R-134a, R-32, R-410A, R-404A)", "fridges, heat pumps, air conditioning"),
                 ("PTFE and fluoropolymers", "non-stick coatings, seals, membranes"),
                 ("PFAS (PFOS, PFOA and thousands more)", "firefighting foam, textiles, food packaging"),
                 ("Lithium hexafluorophosphate (LiPF₆)", "electrolyte salt in lithium-ion batteries")],
  climate=[("HFCs", "e.g. HFC-134a, 100-year GWP 1,300 (AR5)"),
           ("Sulfur hexafluoride (SF₆) and nitrogen trifluoride (NF₃)", "very high GWP, very long-lived"),
           ("Trifluoroacetic acid (TFA)", "a breakdown product of some newer refrigerants, building up in water")],
 ),
)

F['Sb'] = dict(
 post='/blog/2026/11/antimony-the-critical-mineral-nobody-has-heard-of/',
 pdf='/assets/briefings/elements/antimony-briefing.pdf',
 env="Antimony reaches soil from shooting ranges, brake-pad wear on busy roads, smelting and landfill. It is toxic in a similar way to arsenic, its neighbour in the table, though less potent. Small amounts migrate from PET plastic, which is made with an antimony catalyst.",
 eng="Most antimony goes into flame retardants (antimony trioxide boosts brominated retardants in plastics and textiles), lead-acid battery grids, PET catalysts, solar-panel glass and ammunition. It is on the UK critical minerals list. China dominates refining and has controlled exports since September 2024.",
 geo="The main ore is stibnite (antimony sulfide), found with gold, lead and silver deposits. Supply is concentrated in China, Russia and Tajikistan.",
 chem="Group 15, period 5; a metalloid. Brittle, silvery and a poor conductor. Common states are +3 and +5. Stibine (SbH₃) is a very toxic gas that can form when antimony alloys meet acid, as in battery charging.",
 land="Antimony is a contaminant to look for at shooting grounds, battery recycling and scrap yards, smelters and old landfill. Roadside soils and drain sediments on busy routes carry antimony from brake dust.",
 safety=dict(
  coshh="COSHH applies to antimony and its compounds. The main workplace risks are dust and fume (from smelting, battery and alloy work) and stibine gas.",
  classes=[
   ("Antimony (metal)", "No harmonised CLP entry for the massive metal; suppliers classify powder by its hazards (check the safety data sheet)."),
   ("Antimony compounds (group entry, with listed exceptions)", "Acute Tox. 4 H302 + H332 (harmful if swallowed or inhaled); Aquatic Chronic 2 H411. Harmonised (CLP Annex VI)."),
   ("Diantimony trioxide (Sb₂O₃)", "Carc. 2 H351 (suspected of causing cancer). Harmonised (CLP Annex VI)."),
  ],
  wels=[
   ("Antimony and compounds except stibine (as Sb)", "0.5 mg/m³ LTEL"),
   ("Stibine", "0.1 ppm LTEL (check)"),
  ],
  un=[
   ("UN2871", "Antimony powder", "6.1"),
   ("UN2676", "Stibine", "2.3 (2.1)"),
   ("UN1733", "Antimony trichloride", "8"),
   ("UN1730", "Antimony pentachloride, liquid", "8"),
  ],
  risks="Solid antimony is of low hazard to handle. Its dust and fume irritate the lungs and skin ('antimony spots'), and long exposure to the trioxide dust is a suspected cause of lung cancer. Stibine gas is acutely toxic.",
 ),
 compounds=dict(
  nature=[("Stibnite (Sb₂S₃)", "the main ore"), ("Antimonate and antimonite ions", "the mobile forms in soil water")],
  manufacturing=[("Antimony trioxide (Sb₂O₃)", "flame-retardant synergist; PET catalyst; glass fining"),
                 ("Lead–antimony alloys", "battery grids, cable sheathing, shot"),
                 ("Antimony sulfide", "friction modifier in brake pads; match heads"),
                 ("Sodium antimonate", "clarifying agent in glass, including solar glass")],
  climate=[("No antimony greenhouse gas", "its climate link is supply: solar glass, storage batteries and grid equipment"),
           ("Flame retardants in insulation and cables", "part of the building and electrification supply chain")],
 ),
)

F['Mg'] = dict(
 post='/blog/2026/11/magnesium-the-metal-in-every-leaf-and-the-cause-of-grass-staggers/',
 pdf='/assets/briefings/elements/magnesium-briefing.pdf',
 env="Every chlorophyll molecule holds a magnesium atom, so no magnesium means no photosynthesis. Magnesium-rich rocks such as basalt and olivine absorb CO₂ slowly as they weather, which is the basis of 'enhanced rock weathering' as a carbon removal method, still at the research and trial stage.",
 eng="Magnesium metal is a third lighter than aluminium and is alloyed for car parts, laptops and aircraft. Most is made in China by the Pidgeon process, which is energy and carbon intensive. Magnesium oxide is used in refractories, animal feed, cements and water treatment. Magnesium and magnesite are on the UK 2024 critical minerals list.",
 geo="Magnesium is the eighth most abundant element in the crust. It is found in dolomite, magnesite, olivine, serpentine and the basalts of the Antrim Plateau, and in seawater as magnesium chloride and sulfate.",
 chem="Group 2, period 3; an alkaline earth metal. Burns with a dazzling white flame and keeps burning in carbon dioxide and steam, so water makes a magnesium fire worse. Forms Mg²⁺ ions in water.",
 land="Cattle and sheep cannot store magnesium. Fast-growing spring grass, high potassium and heavy nitrogen lower the magnesium cows take in, causing grass tetany (staggers), which can kill within hours. Magnesian (dolomitic) lime supplies magnesium as well as raising pH.",
 safety=dict(
  coshh="COSHH applies to magnesium dust and fume and to magnesium oxide. The bigger risk is fire: magnesium powder and swarf are flammable and react with water to release hydrogen.",
  classes=[
   ("Magnesium powder (pyrophoric)", "Pyr. Sol. 1 H250; Water-react. 1 H260 (releases flammable gas with water). Harmonised (CLP Annex VI)."),
   ("Magnesium powder or turnings (stabilised)", "Flam. Sol. 1 H228; Water-react. 2 H261. Harmonised (CLP Annex VI)."),
   ("Magnesium (massive metal)", "Not classified in solid form, but it burns once alight."),
  ],
  wels=[
   ("Magnesium oxide (as Mg)", "10 mg/m³ LTEL inhalable dust; 4 mg/m³ respirable dust and fume (check)"),
  ],
  un=[
   ("UN1418", "Magnesium powder or magnesium alloys powder", "4.3 (4.2)"),
   ("UN1869", "Magnesium or magnesium alloys (>50% Mg) in pellets, turnings or ribbons", "4.1"),
   ("UN1474", "Magnesium nitrate", "5.1"),
  ],
  risks="Never use water or a CO₂ extinguisher on burning magnesium; use dry sand or a Class D powder. Machining swarf and fine powder are the main fire risks in workshops. Magnesium compounds in fertiliser and feed are of low hazard.",
 ),
 compounds=dict(
  nature=[("Chlorophyll", "the green pigment in every leaf"), ("Dolomite (CaMg(CO₃)₂) and magnesite (MgCO₃)", "carbonate rocks"),
          ("Olivine and serpentine", "magnesium silicates in basalts and ultramafic rocks"),
          ("Magnesium in seawater", "about 1.3 g per litre")],
  manufacturing=[("Magnesium oxide (MgO)", "refractories, feed supplements, cements"),
                 ("Magnesium sulfate (kieserite, Epsom salt)", "fertiliser and medicine"),
                 ("Magnesium hydroxide", "flame retardant and wastewater treatment"),
                 ("Magnesium chloride", "de-icing and dust suppression"),
                 ("Magnesium alloys", "light-weighting of vehicles and electronics")],
  climate=[("Calcining magnesite", "releases process CO₂, as with limestone for cement"),
           ("Enhanced rock weathering", "spreading crushed basalt or olivine on land to draw down CO₂; research stage"),
           ("Light-weighting", "lighter vehicles use less energy")],
 ),
)

F['C'] = dict(
 post='/blog/2026/11/carbon-the-element-we-count/',
 pdf='/assets/briefings/elements/carbon-briefing.pdf',
 env="Carbon dioxide and methane are the two largest causes of human-made warming. In Northern Ireland in 2023, carbon dioxide made up 61.5% of greenhouse gas emissions and methane 30.2%. Soils, peat and forests hold far more carbon than the air, and can lose it fast when drained or ploughed.",
 eng="Carbon is the backbone of fuels, plastics, steel (as the reducing agent and alloying element), cement chemistry (limestone) and carbon fibre. Graphite is a battery anode material and is on the UK critical minerals list. Carbon capture aims to keep CO₂ from industrial sources out of the air.",
 geo="Carbon is stored in limestone and chalk (the largest store), coal, oil, gas, peat and diamonds. Northern Ireland has chalk and limestone, lignite near Lough Neagh, and extensive blanket and raised bogs.",
 chem="Group 14, period 2. Carbon forms four bonds and long chains and rings with itself, giving millions of organic compounds. Forms include graphite, diamond, graphene and fullerenes. Carbon-14 dating uses its radioactive isotope.",
 land="Agriculture produced 31.4% of Northern Ireland's emissions in 2024, mostly methane from cattle and sheep. Peat soils store a large share of Northern Ireland's land carbon; drained peat is a net source of CO₂. Soil carbon is measured slowly and is easy to lose.",
 safety=dict(
  coshh="COSHH applies to carbon dusts (carbon black, graphite, coal) and to carbon monoxide and carbon dioxide. Most deaths come from carbon monoxide (combustion in poorly ventilated spaces) and from CO₂ build-up in cellars, silos and slurry stores.",
  classes=[
   ("Carbon: graphite, diamond", "Not classified."),
   ("Carbon black", "No harmonised CLP classification; IARC Group 2B. Combustible dust."),
   ("Activated carbon and charcoal", "May be self-heating (class 4.2 for transport) depending on test results."),
  ],
  wels=[
   ("Carbon black", "3.5 mg/m³ LTEL; 7 mg/m³ STEL"),
   ("Carbon dioxide", "5,000 ppm LTEL; 15,000 ppm STEL"),
   ("Carbon monoxide", "20 ppm LTEL; 100 ppm STEL (from 2018; check)"),
   ("Graphite", "10 mg/m³ inhalable; 4 mg/m³ respirable (check)"),
  ],
  un=[
   ("UN1361", "Carbon, animal or vegetable origin (e.g. charcoal)", "4.2"),
   ("UN1362", "Carbon, activated", "4.2"),
   ("UN1013", "Carbon dioxide", "2.2"),
   ("UN2187", "Carbon dioxide, refrigerated liquid", "2.2"),
   ("UN1845", "Carbon dioxide, solid (dry ice)", "9"),
   ("UN1016", "Carbon monoxide, compressed", "2.3 (2.1)"),
   ("UN1971", "Methane, compressed (or natural gas)", "2.1"),
   ("UN1972", "Methane, refrigerated liquid (LNG)", "2.1"),
  ],
  risks="Elemental carbon is low in toxicity, but its dusts can explode and charcoal can self-heat in storage. Carbon monoxide gives no warning. Carbon dioxide is heavier than air and collects in pits and slurry tanks; dry ice in a vehicle or cold room can reach dangerous levels.",
 ),
 compounds=dict(
  nature=[("Carbon dioxide (CO₂)", "about 0.04% of air and rising"), ("Methane (CH₄)", "from wetlands, ruminants and landfill"),
          ("Calcium carbonate (CaCO₃)", "limestone, chalk, shells"), ("Soil organic matter and peat", "the land carbon store")],
  manufacturing=[("Coke and coal", "reducing agent in blast-furnace steel"), ("Clinker (from limestone)", "cement; covered by EU and UK CBAM"),
                 ("Carbon black", "tyres, inks, plastics"), ("Graphite", "battery anodes, electrodes, lubricants"),
                 ("Plastics and fuels", "almost all made from fossil carbon"), ("Biochar", "charcoal made for soils")],
  climate=[("Carbon dioxide", "GWP 1 by definition; lasts centuries to millennia"),
           ("Methane", "100-year GWP 28 (AR5, as used in the UK inventory); lasts about 12 years"),
           ("Black carbon (soot)", "warms by absorbing sunlight and darkening snow"),
           ("Carbon monoxide", "not a direct greenhouse gas, but extends methane's life")],
 ),
)

F['Rn'] = dict(
 post='/blog/2026/11/radon-the-gas-from-the-ground-a-tighter-house-can-trap/',
 pdf='/assets/briefings/elements/radon-briefing.pdf',
 env="Radon is a radioactive gas that seeps from the ground into buildings. Breathing its decay products over years raises the risk of lung cancer, especially for smokers. Outdoors it disperses harmlessly; indoors it can build up.",
 eng="Radon protection in new buildings uses a gas-resistant membrane, with a sump or ventilated sub-floor in higher-risk areas. Existing buildings are fixed with a radon sump and fan or better under-floor ventilation. Making buildings more airtight to save energy can raise indoor radon unless ventilation is designed in.",
 geo="Radon-222 comes from the decay of uranium in rocks and soils, via radium. Levels follow geology; Northern Ireland's radon potential map (UKHSA, GSNI and BGS) shows the areas affected. Radon also dissolves in groundwater, so private wells can carry it.",
 chem="Group 18, period 6; the heaviest naturally occurring noble gas. Chemically almost inert. Radon-222 has a half-life of 3.8 days and decays through short-lived polonium, lead and bismuth isotopes that stick to dust and lodge in the lungs.",
 land="Whether a site is in a radon affected area decides what protection a new building needs under the Building Regulations (Northern Ireland). Workplaces in affected areas should test, and employers must act where annual averages exceed 300 Bq/m³ under the Ionising Radiations Regulations (Northern Ireland) 2017.",
 safety=dict(
  coshh="COSHH does not cover the radiation hazard of radon; the Ionising Radiations Regulations (Northern Ireland) 2017 do. Radioactive substances also fall outside CLP classification.",
  classes=[
   ("Radon", "No CLP classification (radioactive substances are outside CLP). Regulated as a source of ionising radiation."),
  ],
  wels=[
   ("Workplaces (IRR NI 2017)", "Reference level 300 Bq/m³ annual average; employers must act above it"),
   ("Homes (UKHSA)", "Action level 200 Bq/m³; target level 100 Bq/m³"),
   ("UK average in homes", "about 20 Bq/m³ (UKHSA)"),
  ],
  un=[
   ("No specific UN number", "Radon is not consigned as a substance. Any radioactive material in transport is Class 7, e.g. UN2910 (excepted package). Passive radon test detectors are not dangerous goods.", "7 (if any)"),
  ],
  risks="Radon is colourless, odourless and tasteless: only a test shows the level. The risk is long-term lung cancer, not acute poisoning. Smokers exposed to radon face a much higher risk than non-smokers.",
 ),
 compounds=dict(
  nature=[("Uranium-238 and radium-226", "the parents of radon in rocks and soil"),
          ("Radon progeny: polonium-218, lead-214, bismuth-214, polonium-214", "the short-lived decay products that deliver the lung dose"),
          ("Lead-210 and polonium-210", "longer-lived decay products in soils and dust"),
          ("Thoron (radon-220)", "a short-lived radon isotope from thorium")],
  manufacturing=[("Radon has no industrial compounds", "it is almost chemically inert"),
                 ("Building materials", "some stone and phosphogypsum carry radium; most UK materials are low")],
  climate=[("No climate effect", "radon is not a greenhouse gas"),
           ("Atmospheric tracer", "because it comes only from land, radon is used by scientists to track air masses and check greenhouse gas estimates"),
           ("Energy retrofits", "sealing homes without ventilation can raise indoor radon")],
 ),
)

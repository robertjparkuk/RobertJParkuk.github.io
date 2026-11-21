"""Element briefings, part D: elements 93-118, from neptunium to oganesson.
Half-lives are for the longest-lived known isotope and are rounded; for the
superheavy elements they are approximate and revised as new isotopes are made.
Checked 21 November 2026."""

_none = dict(climate="No role.", pollution="None: it exists only in tiny amounts in research labs.")

B = {
'Np': dict(
 nature="Traces in uranium ores from neutron capture.",
 climate="By-product of nuclear power.",
 pollution="Neptunium-237 is a long-lived part of high-level nuclear waste and matters for deep disposal.",
 manufacturing="Made in reactors; used to produce plutonium-238 for space power.",
 health="Radioactive and toxic.",
 hazards="Radioactive; IRR applies.",
 discovery="Made at Berkeley in 1940 by McMillan and Abelson, the first element beyond uranium; named after Neptune. Neptunium-237 half-life 2.1 million years."),
'Pu': dict(
 nature="Essentially absent; tiny natural traces and fallout from weapons tests.",
 climate="Can be recycled as MOX nuclear fuel.",
 pollution="Discharges from Sellafield left plutonium in Irish Sea sediments; the UK holds a large civil plutonium stockpile.",
 manufacturing="Nuclear fuel and weapons; plutonium-238 powers deep-space probes.",
 health="Highly toxic if inhaled; lodges in bone and lungs.",
 hazards="Radioactive; fissile material is tightly controlled.",
 discovery="Made at Berkeley in 1940–41 by Seaborg and colleagues; named after Pluto. Plutonium-244 half-life about 80 million years; plutonium-239 24,000 years."),
'Am': dict(
 nature="Absent from nature.",
 climate="By-product of nuclear power.",
 pollution="A long-lived part of nuclear waste; old smoke detectors need correct disposal.",
 manufacturing="Ionisation smoke detectors (americium-241); neutron sources for soil-moisture and oil-well gauges.",
 health="Radioactive; harmful if taken into the body.",
 hazards="Radioactive; sealed sources regulated.",
 discovery="Made at Chicago in 1944 by Seaborg's team; named after the Americas. Americium-243 half-life about 7,400 years; americium-241 432 years."),
'Cm': dict(
 nature="Absent from nature.",
 climate="By-product of nuclear power.",
 pollution="Part of long-lived nuclear waste.",
 manufacturing="Alpha sources in instruments, including X-ray spectrometers on Mars rovers.",
 health="Radioactive.",
 hazards="Radioactive.",
 discovery="Made at Berkeley in 1944 by Seaborg, James and Ghiorso; named after Marie and Pierre Curie. Curium-247 half-life about 16 million years."),
'Bk': dict(
 nature="Absent from nature.", **_none,
 manufacturing="Made in milligram amounts in research reactors; used as a target to make heavier elements, including tennessine.",
 health="Radioactive.",
 hazards="Radioactive.",
 discovery="Made at Berkeley in 1949; named after Berkeley. Berkelium-247 half-life about 1,400 years."),
'Cf': dict(
 nature="Absent from nature.", climate="No role.",
 pollution="Sealed neutron sources must be controlled and disposed of properly.",
 manufacturing="Californium-252 neutron sources start up reactors, find oil and water in boreholes and check aircraft parts.",
 health="Strong neutron emitter; radioactive.",
 hazards="Radioactive; sealed sources regulated.",
 discovery="Made at Berkeley in 1950; named after California. Californium-251 half-life about 900 years; californium-252 2.6 years."),
'Es': dict(
 nature="Absent from nature.", **_none,
 manufacturing="Research only; made in microgram amounts.",
 health="Radioactive.",
 hazards="Radioactive.",
 discovery="Found in 1952 in debris from the first hydrogen bomb test ('Ivy Mike'); named after Albert Einstein. Einsteinium-252 half-life about 470 days."),
'Fm': dict(
 nature="Absent from nature.", **_none,
 manufacturing="Research only; the heaviest element that can be made by neutron capture in reactors.",
 health="Radioactive.",
 hazards="Radioactive.",
 discovery="Found in the same 1952 'Ivy Mike' debris; named after Enrico Fermi. Fermium-257 half-life about 100 days."),
'Md': dict(
 nature="Absent from nature.", **_none,
 manufacturing="Research only; made a few atoms at a time.",
 health="Radioactive.",
 hazards="Radioactive.",
 discovery="Made at Berkeley in 1955, at first 17 atoms; named after Dmitri Mendeleev. Mendelevium-258 half-life about 51 days."),
'No': dict(
 nature="Absent from nature.", **_none,
 manufacturing="Research only.",
 health="Radioactive.",
 hazards="Radioactive.",
 discovery="Claimed in Stockholm in 1957 and confirmed at Dubna in the 1960s; named after Alfred Nobel. Nobelium-259 half-life about 1 hour."),
'Lr': dict(
 nature="Absent from nature.", **_none,
 manufacturing="Research only.",
 health="Radioactive.",
 hazards="Radioactive.",
 discovery="Made at Berkeley in 1961 (with later Dubna work); named after Ernest Lawrence, inventor of the cyclotron. Lawrencium-266 half-life about 11 hours."),
'Rf': dict(
 nature="Absent from nature.", **_none,
 manufacturing="Research only. The first transactinide: its chemistry was tested one atom at a time and behaves like hafnium.",
 health="Never made in amounts that could affect anyone.",
 hazards="Radioactive; exists for about an hour at most.",
 discovery="Reported at Dubna (1964) and Berkeley (1969); named after Ernest Rutherford. Rutherfordium-267 half-life about 1–2 hours."),
'Db': dict(
 nature="Absent from nature.", **_none,
 manufacturing="Research only; single-atom chemistry shows it behaves like tantalum and niobium.",
 health="Never made in harmful amounts.",
 hazards="Radioactive.",
 discovery="Reported at Dubna (1968) and Berkeley (1970); named after Dubna, home of the Joint Institute for Nuclear Research. Dubnium-268 half-life about a day."),
'Sg': dict(
 nature="Absent from nature.", **_none,
 manufacturing="Research only; behaves like tungsten in single-atom experiments.",
 health="Never made in harmful amounts.",
 hazards="Radioactive; minutes at most.",
 discovery="Made at Berkeley in 1974; named after Glenn Seaborg, the first element named after a living person. Longest-lived isotopes last minutes."),
'Bh': dict(
 nature="Absent from nature.", **_none,
 manufacturing="Research only; behaves like rhenium.",
 health="Never made in harmful amounts.",
 hazards="Radioactive.",
 discovery="Made at GSI, Darmstadt, in 1981; named after Niels Bohr. Longest-lived isotopes last about a minute."),
'Hs': dict(
 nature="Absent from nature.", **_none,
 manufacturing="Research only; forms a volatile tetroxide like osmium, measured one atom at a time.",
 health="Never made in harmful amounts.",
 hazards="Radioactive; seconds.",
 discovery="Made at GSI in 1984; named after Hesse, the German state. Longest-lived isotopes last about 10 seconds."),
'Mt': dict(
 nature="Absent from nature.", **_none,
 manufacturing="Research only; its chemistry has not been studied.",
 health="Never made in harmful amounts.",
 hazards="Radioactive; seconds.",
 discovery="Made at GSI in 1982; named after Lise Meitner, co-discoverer of nuclear fission. Longest-lived isotopes last a few seconds."),
'Ds': dict(
 nature="Absent from nature.", **_none,
 manufacturing="Research only.",
 health="Never made in harmful amounts.",
 hazards="Radioactive; seconds.",
 discovery="Made at GSI in 1994; named after Darmstadt. Longest-lived isotope lasts about 10 seconds."),
'Rg': dict(
 nature="Absent from nature.", **_none,
 manufacturing="Research only; predicted to be a heavier relative of gold.",
 health="Never made in harmful amounts.",
 hazards="Radioactive.",
 discovery="Made at GSI in 1994; named after Wilhelm Röntgen, discoverer of X-rays. Longest-lived isotopes last up to a couple of minutes."),
'Cn': dict(
 nature="Absent from nature.", **_none,
 manufacturing="Research only; single-atom experiments suggest it is unusually volatile, like mercury.",
 health="Never made in harmful amounts.",
 hazards="Radioactive.",
 discovery="Made at GSI in 1996; named after Nicolaus Copernicus. Copernicium-285 half-life about 30 seconds."),
'Nh': dict(
 nature="Absent from nature.", **_none,
 manufacturing="Research only.",
 health="Never made in harmful amounts.",
 hazards="Radioactive; seconds.",
 discovery="Made at RIKEN, Japan, from 2004; the first element discovered in Asia, named after Nihon (Japan). Longest-lived isotope lasts about 10 seconds."),
'Fl': dict(
 nature="Absent from nature.", **_none,
 manufacturing="Research only; experiments test whether it behaves like a metal or a volatile, near-noble element.",
 health="Never made in harmful amounts.",
 hazards="Radioactive; seconds.",
 discovery="Made at Dubna from 1998–99 with Livermore; named after the Flerov Laboratory. Longest-lived isotopes last a few seconds."),
'Mc': dict(
 nature="Absent from nature.", **_none,
 manufacturing="Research only.",
 health="Never made in harmful amounts.",
 hazards="Radioactive; under a second.",
 discovery="Made at Dubna from 2003 with Livermore; named after the Moscow region. Longest-lived isotope lasts under a second."),
'Lv': dict(
 nature="Absent from nature.", **_none,
 manufacturing="Research only.",
 health="Never made in harmful amounts.",
 hazards="Radioactive; fractions of a second.",
 discovery="Made at Dubna in 2000 with Livermore; named after Lawrence Livermore National Laboratory. Longest-lived isotope lasts well under a second."),
'Ts': dict(
 nature="Absent from nature.", **_none,
 manufacturing="Research only; made by firing calcium at berkelium from Oak Ridge.",
 health="Never made in harmful amounts.",
 hazards="Radioactive; hundredths of a second.",
 discovery="Made at Dubna in 2010 with Oak Ridge and Vanderbilt; named after Tennessee. Longest-lived isotope lasts tens of milliseconds."),
'Og': dict(
 nature="Absent from nature.", **_none,
 manufacturing="Research only; only a handful of atoms have ever been made. Predicted to be a solid, unlike the other noble gases.",
 health="Never made in harmful amounts.",
 hazards="Radioactive; under a millisecond.",
 discovery="Made at Dubna in 2002–06 with Livermore; named after Yuri Oganessian, the second element named after a living person. Oganesson-294 half-life under a millisecond. It completes period 7 and the table as it stands."),
}

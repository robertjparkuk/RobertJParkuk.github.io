"""Build the dashboard that accompanies the briefing "Faith, reason and the common home"
(Catholic Church in science, business and the environment), 9 November 2026.
Reuses the helpers and styling of build.py. Every figure comes from the sources cited;
derived figures are labelled.
Usage: python3 build_catholic.py <repo_root>
"""
import sys, os
ROOT = sys.argv[1]
_src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'build.py'), encoding='utf-8').read()
exec(_src[:_src.index('D = {}')])

SRC.update({
 'fides': ('Catholic Church Statistics 2026 (Agenzia Fides, 16 October 2026)', 'https://fides.org/en/stats'),
 'btr': ('Vatican City State First Biennial Transparency Report to the UNFCCC (December 2024)', 'https://unfccc.int/sites/default/files/resource/Vatican%20City%20State%20BTR%20-%20December%202024.pdf'),
 'ndc25': ('Vatican City State Nationally Determined Contribution (September 2025)', 'https://unfccc.int/sites/default/files/2025-09/Holy%20See_NDC%202035_September%202025.pdf'),
 'ndc23': ('Vatican City State Nationally Determined Contribution (May 2023)', 'https://unfccc.int/sites/default/files/NDC/2023-05/Vatican%20City%20State%20NDCs%20-%20May%202023.pdf'),
 'agri': ('Ratification of the Italy–Holy See agrivoltaic agreement, A.C. 2759 (Italian Chamber of Deputies)', 'https://temi.camera.it/leg19/provvedimento/ratifica-ed-esecuzione-dell-accordo-tra-la-repubblica-italiana-e-la-santa-sede-per-un-impianto-agrivoltaico-a-santa-maria-di-galeria-fatto-a-roma-il-31-luglio-2025.html'),
 'vnsun': ('Pope orders construction of agrivoltaic plant for the Vatican (Vatican News, 26 June 2024)', 'https://www.vaticannews.va/en/pope/news/2024-06/pope-orders-construction-of-agrivoltaic-plant-for-the-vatican.html'),
 'lsap': ('Laudato Si\' Action Platform five-year report (Vatican News, November 2026)', 'https://www.vaticannews.va/en/vatican-city/news/2026-11/laudato-si-platform-5-year-report-digital-atlas-press-conference.html'),
 'vo': ('Vatican Observatory media kit 2026', 'https://www.vaticanobservatory.org/wp-content/uploads/2025/12/VO-Media-Kit-2026a.pdf'),
 'mendel': ("Mendel's discovery of the Mendelian ratios (History of Information)", 'https://historyofinformation.com/detail.php?entryid=3571'),
 'pacioli': ('Luca Pacioli, Dictionary of Scientific Biography (Encyclopedia.com)', 'https://www.encyclopedia.com/doc/1G2-2830903265.html'),
 'rn': ('Rerum novarum (Leo XIII, 15 May 1891)', 'https://www.vatican.va/content/leo-xiii/en/encyclicals/documents/hf_l-xiii_enc_15051891_rerum-novarum.html'),
 'ls': ("Laudato si' (Pope Francis, 2015)", 'https://www.vatican.va/content/francesco/en/encyclicals/documents/papa-francesco_20150524_enciclica-laudato-si.html'),
 'ie': ("Statement on divestment from fossil fuels (Irish Catholic Bishops' Conference, 24 August 2018)", 'https://www.catholicbishops.ie/2018/08/24/statement-by-bishop-william-crean-announcing-the-decision-of-the-bishops-conference-to-divest-from-fossil-fuels/'),
 'galileo': ("The Church's most recent attempt to dispel the Galileo myth (G. Coyne SJ, Vatican Observatory)", 'https://www.vaticanobservatory.org/wp-content/uploads/2017/01/Galileo_ed._McMullin.pdf'),
 'apsa': ('APSA report 2025 (InfoVaticana, 4 August 2026)', 'https://infovaticana.com/it/2026/08/04/rapporto-apsa-2025-il-patrimonio-netto-della-santa-sede-ammonta-a-2686-milioni-di-euro/'),
})

schools = [('Primary schools', 36.314935, '36.3m pupils'), ('Secondary schools', 20.340808, '20.3m pupils'),
           ('Kindergartens', 7.480373, '7.5m pupils'), ('University institutes', 4.091087, '4.1m students')]
health = [('Homes for elderly, chronically ill or disabled', 16263, None), ('Dispensaries', 13646, None), ('Marriage counselling centres', 10624, None),
          ('Crèches', 10352, None), ('Orphanages', 8138, None), ('Hospitals', 5397, None), ('Social rehabilitation centres', 3194, None),
          ('Homes for people with leprosy', 468, None)]
people = [('Women religious', 580131, None), ('Priests', 407421, None), ('Major seminarians', 103604, None), ('Bishops', 5525, None)]
ghg = [(str(y), v, f'{v*1000:,.0f} t') for y, v in [(2011, 19.33), (2012, 17.20), (2013, 18.08), (2014, 17.65), (2015, 17.30), (2016, 16.50),
                                                       (2017, 17.04), (2018, 16.03), (2019, 15.90), (2020, 15.95), (2021, 15.38), (2022, 15.89)]]
ghg.append(('2030 target (−20%)', 15.44, '≈15,440 t'))
ghg.append(('2035 target (−28%)', 13.90, '≈13,900 t'))
mix = [('Vehicles (petrol and diesel)', 71, '11,250 t · 71%'), ('Heating', 22, '3,460 t · 22%'), ('Refrigerant gases (HFCs)', 7, '1,180 t · 7%')]
timeline = [
 ('1494', 'Business', 'Franciscan friar Luca Pacioli prints the first full account of double-entry bookkeeping (Venice)'),
 ('1582', 'Science', 'Gregorian calendar reform, worked out with the Jesuit mathematician Christopher Clavius'),
 ('1603', 'Science', 'Accademia dei Lincei founded in Rome; Galileo becomes a member'),
 ('1865', 'Science', 'Gregor Mendel presents his pea experiments in Brno: the start of genetics'),
 ('1891', 'Business', 'Rerum novarum argues for a living wage and the right to form unions'),
 ('1891', 'Science', 'Leo XIII re-founds the Vatican Observatory; it joins the Carte du Ciel sky survey'),
 ('1927', 'Science', 'Mgr Georges Lemaître proposes the expanding universe'),
 ('1956', 'Business', 'Fr José María Arizmendiarrieta\'s students found the first Mondragon co-operative'),
 ('1992', 'Science', 'John Paul II acknowledges the errors of Galileo\'s judges'),
 ('1993', 'Science', 'Vatican Advanced Technology Telescope opens on Mount Graham, Arizona'),
 ('2008', 'Environment', 'About 2,400 solar panels go on the Paul VI Audience Hall'),
 ('2015', 'Environment', "Laudato si' puts care for creation at the centre of Church teaching"),
 ('2018', 'Environment', 'Irish bishops commit to divest from the top 200 oil and gas companies'),
 ('2022', 'Environment', 'Holy See joins the UN climate convention and the Paris Agreement'),
 ('2022', 'Business', 'Mensuram Bonam: guidance on faith-consistent investing'),
 ('2026', 'Environment', 'Italy–Holy See treaty for the Santa Maria di Galeria agrivoltaic plant comes into force (27 May)'),
]
quiz = [('Which is bigger: Catholic primary-school pupils, or the population of Australia?', 'The pupils: 36.3 million, against about 27 million people in Australia.'),
        ("What is the Vatican's biggest source of emissions?", 'Vehicles, at 71%. Buildings and heating are 22%.'),
        ('Who first set out the laws of heredity?', 'Gregor Mendel, an Augustinian friar, in 1865.'),
        ('How much of the Vatican\'s electricity does it generate itself today?', 'Almost none. It imports it all; the agrivoltaic plant is meant to change that.')]

cards = [
 card('Pupils and students in Catholic education', 'Millions, end of 2024. 230,924 schools in all.', bars(schools, hi=['Primary schools']), ['fides'],
      csv_href(['level', 'pupils_millions'], [[a, b] for a, b, c in schools]), 'catholic-education-2024'),
 card('Health and charity centres', 'Number of institutions, end of 2024. 101,110 in all, including 33,028 "other".', bars(health, hi=['Hospitals']), ['fides'],
      csv_href(['type', 'count'], [[a, b] for a, b, c in health]), 'catholic-health-charity-2024'),
 card('People', 'End of 2024.', bars(people), ['fides'], csv_href(['group', 'count'], [[a, b] for a, b, c in people]), 'catholic-clergy-religious-2024'),
 card("Vatican City State's emissions", 'Thousand tonnes CO₂e, as reported to the UN. Targets are worked out on the restated 2011 base of 19,300 t (derived).', bars(ghg, hi=['2022', '2030 target (−20%)', '2035 target (−28%)'], maxv=20), ['btr', 'ndc23', 'ndc25'],
      csv_href(['year', 'kt_co2e'], [[a, b] for a, b, c in ghg]), 'vatican-ghg-2011-2022'),
 card('Where the Vatican\'s emissions come from, 2022', 'Share of 15,890 t CO₂e. Its electricity is imported and reported as renewable, so it adds nothing here.', bars(mix, hi=['Vehicles (petrol and diesel)'], maxv=100), ['btr'],
      csv_href(['source', 'share_pct'], [[a, b] for a, b, c in mix]), 'vatican-ghg-sources-2022'),
 card('Five centuries in sixteen dates', 'Science, business and environment milestones covered in the briefing.', table(['Year', 'Theme', 'What happened'], timeline),
      ['pacioli', 'vo', 'mendel', 'rn', 'galileo', 'ls', 'ie', 'agri'], csv_href(['year', 'theme', 'event'], timeline), 'church-science-business-environment-timeline', wide=True),
 card('Quick quiz', 'Cover the right-hand column and test yourself.', table(['Question', 'Answer'], quiz), ['fides', 'btr', 'mendel', 'vnsun'], None, None, wide=True),
]
tiles = [tile('Catholics, mid-2024', '1.42bn', '17.8% of the world'), tile('Pupils in Catholic schools', '64.1m', 'Derived: sum of three levels', 'k-good'),
         tile('Hospitals', '5,397', 'Of 101,110 health and charity centres'), tile('Vatican emissions, 2022', '15,890 t', '18% below 2011 (derived)', 'k-good'),
         tile('Vatican share of world emissions', '0.0000432%', '2022, as stated in its NDC'), tile("Laudato Si' Action Platform", '13,600+', 'Participants after five years')]

slug = 'catholic-church-science-environment'
out = page(slug, 'The Catholic Church in numbers: science, business and the environment',
           'The Catholic Church in numbers',
           'Schools, hospitals and science across five centuries, and the carbon footprint of the world\'s smallest state. The figures behind the briefing <b>Faith, reason and the common home</b>.',
           tiles, cards, '/blog/2026/11/catholic-church-science-business-environment/', 'Faith, reason and the common home', '9 November 2026',
           "Dashboard of the Catholic Church's global footprint in schools and health care, its science and business milestones, and Vatican City State's greenhouse gas emissions and targets. By Robert J. Park.")
out = out.replace('checked on 20–21 October 2026', 'checked against the sources cited in the briefing, as at 9 November 2026')
out = out.replace('Figures checked on 21 October 2026, for publication with the issue of', 'Figures as at 9 November 2026, published with the briefing of')
out = out.replace('<p class="k-foot">Commentary:', '<p class="k-foot">Read the briefing:')
open(os.path.join(ROOT, 'tools/dashboards', slug + '.html'), 'w', encoding='utf-8').write(out)
print(slug, len(out))

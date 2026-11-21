"""Periodic table base data: number, symbol, name, standard atomic weight (abridged,
IUPAC; mass number of the longest-lived isotope in brackets where no standard weight
exists) and category. Positions are worked out from the atomic number."""

# Z, symbol, name, weight, category
ELEMENTS = [
 (1,'H','Hydrogen','1.008','nonmetal'),(2,'He','Helium','4.0026','noble-gas'),
 (3,'Li','Lithium','6.94','alkali'),(4,'Be','Beryllium','9.0122','alkaline-earth'),
 (5,'B','Boron','10.81','metalloid'),(6,'C','Carbon','12.011','nonmetal'),
 (7,'N','Nitrogen','14.007','nonmetal'),(8,'O','Oxygen','15.999','nonmetal'),
 (9,'F','Fluorine','18.998','halogen'),(10,'Ne','Neon','20.180','noble-gas'),
 (11,'Na','Sodium','22.990','alkali'),(12,'Mg','Magnesium','24.305','alkaline-earth'),
 (13,'Al','Aluminium','26.982','post-transition'),(14,'Si','Silicon','28.085','metalloid'),
 (15,'P','Phosphorus','30.974','nonmetal'),(16,'S','Sulfur','32.06','nonmetal'),
 (17,'Cl','Chlorine','35.45','halogen'),(18,'Ar','Argon','39.95','noble-gas'),
 (19,'K','Potassium','39.098','alkali'),(20,'Ca','Calcium','40.078','alkaline-earth'),
 (21,'Sc','Scandium','44.956','transition'),(22,'Ti','Titanium','47.867','transition'),
 (23,'V','Vanadium','50.942','transition'),(24,'Cr','Chromium','51.996','transition'),
 (25,'Mn','Manganese','54.938','transition'),(26,'Fe','Iron','55.845','transition'),
 (27,'Co','Cobalt','58.933','transition'),(28,'Ni','Nickel','58.693','transition'),
 (29,'Cu','Copper','63.546','transition'),(30,'Zn','Zinc','65.38','transition'),
 (31,'Ga','Gallium','69.723','post-transition'),(32,'Ge','Germanium','72.630','metalloid'),
 (33,'As','Arsenic','74.922','metalloid'),(34,'Se','Selenium','78.971','nonmetal'),
 (35,'Br','Bromine','79.904','halogen'),(36,'Kr','Krypton','83.798','noble-gas'),
 (37,'Rb','Rubidium','85.468','alkali'),(38,'Sr','Strontium','87.62','alkaline-earth'),
 (39,'Y','Yttrium','88.906','transition'),(40,'Zr','Zirconium','91.224','transition'),
 (41,'Nb','Niobium','92.906','transition'),(42,'Mo','Molybdenum','95.95','transition'),
 (43,'Tc','Technetium','[98]','transition'),(44,'Ru','Ruthenium','101.07','transition'),
 (45,'Rh','Rhodium','102.91','transition'),(46,'Pd','Palladium','106.42','transition'),
 (47,'Ag','Silver','107.87','transition'),(48,'Cd','Cadmium','112.41','transition'),
 (49,'In','Indium','114.82','post-transition'),(50,'Sn','Tin','118.71','post-transition'),
 (51,'Sb','Antimony','121.76','metalloid'),(52,'Te','Tellurium','127.60','metalloid'),
 (53,'I','Iodine','126.90','halogen'),(54,'Xe','Xenon','131.29','noble-gas'),
 (55,'Cs','Caesium','132.91','alkali'),(56,'Ba','Barium','137.33','alkaline-earth'),
 (57,'La','Lanthanum','138.91','lanthanide'),(58,'Ce','Cerium','140.12','lanthanide'),
 (59,'Pr','Praseodymium','140.91','lanthanide'),(60,'Nd','Neodymium','144.24','lanthanide'),
 (61,'Pm','Promethium','[145]','lanthanide'),(62,'Sm','Samarium','150.36','lanthanide'),
 (63,'Eu','Europium','151.96','lanthanide'),(64,'Gd','Gadolinium','157.25','lanthanide'),
 (65,'Tb','Terbium','158.93','lanthanide'),(66,'Dy','Dysprosium','162.50','lanthanide'),
 (67,'Ho','Holmium','164.93','lanthanide'),(68,'Er','Erbium','167.26','lanthanide'),
 (69,'Tm','Thulium','168.93','lanthanide'),(70,'Yb','Ytterbium','173.05','lanthanide'),
 (71,'Lu','Lutetium','174.97','lanthanide'),(72,'Hf','Hafnium','178.49','transition'),
 (73,'Ta','Tantalum','180.95','transition'),(74,'W','Tungsten','183.84','transition'),
 (75,'Re','Rhenium','186.21','transition'),(76,'Os','Osmium','190.23','transition'),
 (77,'Ir','Iridium','192.22','transition'),(78,'Pt','Platinum','195.08','transition'),
 (79,'Au','Gold','196.97','transition'),(80,'Hg','Mercury','200.59','transition'),
 (81,'Tl','Thallium','204.38','post-transition'),(82,'Pb','Lead','207.2','post-transition'),
 (83,'Bi','Bismuth','208.98','post-transition'),(84,'Po','Polonium','[209]','post-transition'),
 (85,'At','Astatine','[210]','halogen'),(86,'Rn','Radon','[222]','noble-gas'),
 (87,'Fr','Francium','[223]','alkali'),(88,'Ra','Radium','[226]','alkaline-earth'),
 (89,'Ac','Actinium','[227]','actinide'),(90,'Th','Thorium','232.04','actinide'),
 (91,'Pa','Protactinium','231.04','actinide'),(92,'U','Uranium','238.03','actinide'),
 (93,'Np','Neptunium','[237]','actinide'),(94,'Pu','Plutonium','[244]','actinide'),
 (95,'Am','Americium','[243]','actinide'),(96,'Cm','Curium','[247]','actinide'),
 (97,'Bk','Berkelium','[247]','actinide'),(98,'Cf','Californium','[251]','actinide'),
 (99,'Es','Einsteinium','[252]','actinide'),(100,'Fm','Fermium','[257]','actinide'),
 (101,'Md','Mendelevium','[258]','actinide'),(102,'No','Nobelium','[259]','actinide'),
 (103,'Lr','Lawrencium','[262]','actinide'),(104,'Rf','Rutherfordium','[267]','transition'),
 (105,'Db','Dubnium','[268]','transition'),(106,'Sg','Seaborgium','[269]','transition'),
 (107,'Bh','Bohrium','[270]','transition'),(108,'Hs','Hassium','[269]','transition'),
 (109,'Mt','Meitnerium','[278]','unknown'),(110,'Ds','Darmstadtium','[281]','unknown'),
 (111,'Rg','Roentgenium','[282]','unknown'),(112,'Cn','Copernicium','[285]','transition'),
 (113,'Nh','Nihonium','[286]','unknown'),(114,'Fl','Flerovium','[289]','unknown'),
 (115,'Mc','Moscovium','[290]','unknown'),(116,'Lv','Livermorium','[293]','unknown'),
 (117,'Ts','Tennessine','[294]','unknown'),(118,'Og','Oganesson','[294]','unknown'),
]

CATEGORY_LABEL = {
 'alkali':'Alkali metal','alkaline-earth':'Alkaline earth metal','transition':'Transition metal',
 'post-transition':'Post-transition metal','metalloid':'Metalloid','nonmetal':'Reactive non-metal',
 'halogen':'Halogen','noble-gas':'Noble gas','lanthanide':'Lanthanide','actinide':'Actinide',
 'unknown':'Properties not yet known',
}

def position(z):
    """(row, col) on an 18-column grid; rows 8 and 9 hold the f-block."""
    if z == 1: return (1, 1)
    if z == 2: return (1, 18)
    if 3 <= z <= 10: return (2, z - 2 if z <= 4 else z + 8)
    if 11 <= z <= 18: return (3, z - 10 if z <= 12 else z)
    if 19 <= z <= 36: return (4, z - 18)
    if 37 <= z <= 54: return (5, z - 36)
    if 55 <= z <= 56: return (6, z - 54)
    if 57 <= z <= 71: return (8, z - 54)      # lanthanides, cols 3-17
    if 72 <= z <= 86: return (6, z - 68)
    if 87 <= z <= 88: return (7, z - 86)
    if 89 <= z <= 103: return (9, z - 86)     # actinides, cols 3-17
    if 104 <= z <= 118: return (7, z - 100)
    raise ValueError(z)

def period_group(z):
    r, c = position(z)
    if r == 8: return 6, None
    if r == 9: return 7, None
    return r, c

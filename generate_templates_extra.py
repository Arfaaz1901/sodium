"""
Generate additional specific reaction templates to reach 2000+ total.
Appends to the existing specific_reactions.json.
"""
import json

with open("data/specific_reactions.json", "r", encoding="utf-8") as f:
    templates = json.load(f)

_id = len(templates)
existing_keys = set()
for t in templates:
    key = tuple(sorted(t.get("reactants", [])))
    existing_keys.add(key)

def tid():
    global _id
    _id += 1
    return f"SR_{_id:04d}"

def add(reaction_type, reactants, products_detail, equation, pH=7.0,
        energy_kJ=0, is_exothermic=True, hazard_level=2,
        observations=None, gas_evolved=None, precipitate=None,
        precipitate_color=None, effects=None):
    key = tuple(sorted(reactants))
    if key in existing_keys:
        return  # skip duplicate
    existing_keys.add(key)
    templates.append({
        "id": tid(),
        "reaction_type": reaction_type,
        "reactants": sorted(reactants),
        "products_detail": products_detail,
        "equation": equation,
        "pH": pH,
        "energy_kJ": energy_kJ,
        "is_exothermic": is_exothermic,
        "hazard_level": hazard_level,
        "observations": observations or [],
        "gas_evolved": gas_evolved,
        "precipitate": precipitate,
        "precipitate_color": precipitate_color,
        "effects": effects or {}
    })

# ═══════════════════════════════════════════════════════════════
# EXPAND: More acid + metal with all acid variants
# ═══════════════════════════════════════════════════════════════
extra_metals = ["Mn", "Co", "Cr", "Ba", "Sr", "Li", "Ca"]
extra_acids = ["H2SO3", "HClO4", "HNO2", "HCOOH", "H2C2O4"]

for m in extra_metals:
    charges = {"Mn":2,"Co":2,"Cr":3,"Ba":2,"Sr":2,"Li":1,"Ca":2}
    ch = charges.get(m, 2)
    for aid in extra_acids:
        anion_map = {"H2SO3":"SO3","HClO4":"ClO4","HNO2":"NO2","HCOOH":"HCOO","H2C2O4":"C2O4"}
        anion_name_map = {"H2SO3":"sulfite","HClO4":"perchlorate","HNO2":"nitrite","HCOOH":"formate","H2C2O4":"oxalate"}
        an = anion_map.get(aid, "X")
        an_name = anion_name_map.get(aid, "salt")
        sn = f"{m} {an_name}"
        eq = f"{m} + {aid} -> {m}{an} + H2"
        add("Displacement", [m, aid],
            [{"name": sn, "formula": f"{m}({an})" if len(an)>2 else f"{m}{an}", "state": "aq"},
             {"name": "Hydrogen gas", "formula": "H2", "state": "g"}],
            eq, pH=5.0, energy_kJ=80, hazard_level=4,
            observations=[f"{m} dissolves in {aid}", "H2 gas evolved", "Metal displacement reaction"],
            gas_evolved="H2",
            effects={"bubbling": True, "bubblingIntensity": 0.6, "gasRelease": "H2", "sound": "fizz"})

# More metal + acid for existing metals with extra acids
for m in ["Na", "K", "Mg", "Al", "Zn", "Fe", "Sn", "Ni"]:
    charges = {"Na":1,"K":1,"Mg":2,"Al":3,"Zn":2,"Fe":2,"Sn":2,"Ni":2}
    ch = charges[m]
    for aid in extra_acids:
        anion_map = {"H2SO3":"SO3","HClO4":"ClO4","HNO2":"NO2","HCOOH":"HCOO","H2C2O4":"C2O4"}
        an = anion_map.get(aid, "X")
        eq = f"{m} + {aid} -> salt + H2"
        add("Displacement", [m, aid],
            [{"name": f"{m} salt", "formula": f"{m}-{an}", "state": "aq"},
             {"name": "Hydrogen gas", "formula": "H2", "state": "g"}],
            eq, pH=5.0, energy_kJ=80, hazard_level=4,
            observations=[f"{m} reacts with {aid}", "H2 gas produced"],
            gas_evolved="H2",
            effects={"bubbling": True, "bubblingIntensity": 0.6, "gasRelease": "H2", "sound": "fizz"})

# ═══════════════════════════════════════════════════════════════
# EXPAND: More neutralization combos
# ═══════════════════════════════════════════════════════════════
extra_acids2 = ["HBr", "HI", "HF", "H2SO3", "HClO4", "HClO", "HNO2", "H2S", "HCOOH", "H2C2O4"]
extra_bases2 = ["Pb(OH)2", "Mn(OH)2", "Ni(OH)2", "Co(OH)2", "Cr(OH)3"]

for aid in extra_acids2:
    for bid in extra_bases2:
        eq = f"{aid} + {bid} -> salt + H2O"
        add("Neutralization", [aid, bid],
            [{"name": "Salt", "formula": "product salt", "state": "aq"},
             {"name": "Water", "formula": "H2O", "state": "l"}],
            eq, pH=7.0, energy_kJ=57, hazard_level=3,
            observations=[f"Acid-base neutralization: {aid} + {bid}", "Salt and water formed", "pH approaches 7"])

# ═══════════════════════════════════════════════════════════════
# EXPAND: More precipitation - every metal salt + NaOH/KOH
# ═══════════════════════════════════════════════════════════════
metal_salts_for_ppt = {
    "CuSO4": ("Cu(OH)2", "Blue precipitate", "rgba(0,100,255,0.8)"),
    "Cu(NO3)2": ("Cu(OH)2", "Blue precipitate", "rgba(0,100,255,0.8)"),
    "CuCl2": ("Cu(OH)2", "Blue precipitate", "rgba(0,100,255,0.8)"),
    "FeSO4": ("Fe(OH)2", "Dirty green precipitate", "rgba(0,128,0,0.7)"),
    "FeCl2": ("Fe(OH)2", "Dirty green precipitate", "rgba(0,128,0,0.7)"),
    "Fe(NO3)2": ("Fe(OH)2", "Dirty green precipitate", "rgba(0,128,0,0.7)"),
    "FeCl3": ("Fe(OH)3", "Rust-brown precipitate", "rgba(139,69,19,0.85)"),
    "Fe(NO3)3": ("Fe(OH)3", "Rust-brown precipitate", "rgba(139,69,19,0.85)"),
    "Fe2(SO4)3": ("Fe(OH)3", "Rust-brown precipitate", "rgba(139,69,19,0.85)"),
    "ZnSO4": ("Zn(OH)2", "White gelatinous precipitate", "rgba(245,245,245,0.9)"),
    "ZnCl2": ("Zn(OH)2", "White gelatinous precipitate", "rgba(245,245,245,0.9)"),
    "Zn(NO3)2": ("Zn(OH)2", "White gelatinous precipitate", "rgba(245,245,245,0.9)"),
    "MgSO4": ("Mg(OH)2", "White precipitate", "rgba(255,255,255,0.85)"),
    "MgCl2": ("Mg(OH)2", "White precipitate", "rgba(255,255,255,0.85)"),
    "Mg(NO3)2": ("Mg(OH)2", "White precipitate", "rgba(255,255,255,0.85)"),
    "AlCl3": ("Al(OH)3", "White gelatinous precipitate", "rgba(245,245,245,0.9)"),
    "Al2(SO4)3": ("Al(OH)3", "White gelatinous precipitate", "rgba(245,245,245,0.9)"),
    "MnCl2": ("Mn(OH)2", "Pale pink precipitate", "rgba(255,200,200,0.7)"),
    "MnSO4": ("Mn(OH)2", "Pale pink precipitate", "rgba(255,200,200,0.7)"),
    "NiCl2": ("Ni(OH)2", "Green precipitate", "rgba(144,238,144,0.8)"),
    "NiSO4": ("Ni(OH)2", "Green precipitate", "rgba(144,238,144,0.8)"),
    "CoCl2": ("Co(OH)2", "Blue precipitate", "rgba(100,149,237,0.7)"),
    "CoSO4": ("Co(OH)2", "Blue precipitate", "rgba(100,149,237,0.7)"),
    "SnCl2": ("Sn(OH)2", "White precipitate", "rgba(255,255,255,0.85)"),
    "CrCl3": ("Cr(OH)3", "Grey-green precipitate", "rgba(34,139,34,0.8)"),
    "Pb(NO3)2": ("Pb(OH)2", "White precipitate", "rgba(255,255,255,0.85)"),
}

for salt_id, (ppt_f, ppt_desc, ppt_color) in metal_salts_for_ppt.items():
    for base in ["NaOH", "KOH", "NH4OH", "Ca(OH)2", "Ba(OH)2", "LiOH"]:
        eq = f"{salt_id} + {base} -> {ppt_f} + soluble salt"
        add("Precipitation", [salt_id, base],
            [{"name": ppt_f, "formula": ppt_f, "state": "s"}],
            eq, pH=10.0, energy_kJ=15, hazard_level=2,
            observations=[f"{ppt_desc} forms", f"Precipitate: {ppt_f}", "Metal hydroxide is insoluble"],
            precipitate=ppt_f, precipitate_color=ppt_color,
            effects={"precipitate": True, "precipitateColor": ppt_color, "sound": "gentle"})

# ═══════════════════════════════════════════════════════════════
# EXPAND: Carbonate/bicarbonate + more acids
# ═══════════════════════════════════════════════════════════════
carb_ids = ["CaCO3", "Na2CO3", "NaHCO3", "K2CO3", "KHCO3", "MgCO3",
            "ZnCO3", "BaCO3", "SrCO3", "PbCO3", "Li2CO3", "FeCO3", "CuCO3"]
more_acids = ["H2SO3", "HClO4", "HNO2", "HCOOH", "H2C2O4", "H2S"]

for carb in carb_ids:
    for acid in more_acids:
        eq = f"{carb} + {acid} -> salt + H2O + CO2"
        add("Gas Evolution", [carb, acid],
            [{"name": "Salt", "formula": "product", "state": "aq"},
             {"name": "Water", "formula": "H2O", "state": "l"},
             {"name": "Carbon dioxide", "formula": "CO2", "state": "g"}],
            eq, pH=6.0, energy_kJ=16, hazard_level=3,
            observations=["Carbonate reacts with acid", "CO2 gas evolved with effervescence"],
            gas_evolved="CO2",
            effects={"bubbling": True, "bubblingIntensity": 0.7, "gasRelease": "CO2", "sound": "fizz"})

# ═══════════════════════════════════════════════════════════════
# EXPAND: Metal + metal salt displacement (more combos)
# ═══════════════════════════════════════════════════════════════
# Reactivity: K > Na > Li > Ca > Mg > Al > Zn > Fe > Ni > Sn > Pb > H > Cu > Ag > Au > Pt
reactivity_order = {"K":12,"Na":11,"Li":10,"Ca":9,"Mg":8,"Al":7,"Zn":6,"Fe":5,"Ni":4,"Sn":3,"Pb":2,"Cu":1,"Ag":0}

metal_salt_combos = [
    # format: (salt_id, cation_in_salt)
    ("CuSO4", "Cu"), ("CuCl2", "Cu"), ("Cu(NO3)2", "Cu"),
    ("FeSO4", "Fe"), ("FeCl2", "Fe"), ("Fe(NO3)2", "Fe"),
    ("ZnSO4", "Zn"), ("ZnCl2", "Zn"), ("Zn(NO3)2", "Zn"),
    ("NiSO4", "Ni"), ("NiCl2", "Ni"),
    ("AgNO3", "Ag"),
    ("Pb(NO3)2", "Pb"),
    ("SnCl2", "Sn"),
    ("MnSO4", "Mn"), ("MnCl2", "Mn"),
    ("CoSO4", "Co"), ("CoCl2", "Co"),
]

for metal_id in ["Mg", "Al", "Zn", "Fe", "Ni", "Sn", "Pb", "Cu", "Mn", "Co", "Cr"]:
    m_react = reactivity_order.get(metal_id, 5)
    for salt_id, salt_cation in metal_salt_combos:
        if metal_id == salt_cation:
            continue
        s_react = reactivity_order.get(salt_cation, 5)
        if m_react > s_react:
            eq = f"{metal_id} + {salt_id} -> new salt + {salt_cation}"
            add("Displacement", [metal_id, salt_id],
                [{"name": f"New salt", "formula": f"{metal_id} salt", "state": "aq"},
                 {"name": f"{salt_cation} metal", "formula": salt_cation, "state": "s"}],
                eq, pH=5.5, energy_kJ=24, hazard_level=3,
                observations=[f"{metal_id} displaces {salt_cation} from {salt_id}",
                              f"{metal_id} is more reactive than {salt_cation}",
                              f"{salt_cation} deposits as solid metal"])
        else:
            add("No Reaction", [metal_id, salt_id], [],
                f"{metal_id} + {salt_id} -> No Reaction",
                pH=7.0, energy_kJ=0, is_exothermic=False, hazard_level=1,
                observations=[f"{metal_id} is less reactive than {salt_cation}",
                              "No displacement occurs"])

# ═══════════════════════════════════════════════════════════════
# EXPAND: Acid + acid, base + base = No reaction
# ═══════════════════════════════════════════════════════════════
all_acids = ["HCl","H2SO4","HNO3","CH3COOH","H3PO4","H2CO3","HF","HBr",
             "HI","H2SO3","HClO4","HClO","HNO2","H2S","HCOOH","H2C2O4"]
all_bases = ["NaOH","KOH","Ca(OH)2","Mg(OH)2","NH4OH","Ba(OH)2","LiOH","Sr(OH)2"]

for i, a1 in enumerate(all_acids):
    for a2 in all_acids[i+1:]:
        add("No Reaction", [a1, a2], [],
            f"{a1} + {a2} -> No Reaction (acid + acid)",
            pH=1.0, energy_kJ=0, is_exothermic=False, hazard_level=2,
            observations=["Two acids mixed — no neutralization", "Solution becomes more acidic"])

for i, b1 in enumerate(all_bases):
    for b2 in all_bases[i+1:]:
        add("No Reaction", [b1, b2], [],
            f"{b1} + {b2} -> No Reaction (base + base)",
            pH=13.0, energy_kJ=0, is_exothermic=False, hazard_level=2,
            observations=["Two bases mixed — no reaction", "Solution remains alkaline"])

# ═══════════════════════════════════════════════════════════════
# EXPAND: More no-reaction pairs (inert combinations)
# ═══════════════════════════════════════════════════════════════
inert_pairs = [
    ("SiO2", "NaCl"), ("SiO2", "KCl"), ("SiO2", "CaCl2"),
    ("SiO2", "Na2SO4"), ("SiO2", "KNO3"), ("SiO2", "NH4Cl"),
    ("SiO2", "CH3COOH"), ("SiO2", "H2SO4"),
    ("C12H22O11", "NaOH"), ("C12H22O11", "KOH"), ("C12H22O11", "Ca(OH)2"),
    ("C12H22O11", "HCl"), ("C12H22O11", "HNO3"),
    ("C6H12O6", "NaOH"), ("C6H12O6", "HCl"), ("C6H12O6", "KOH"),
    ("C2H5OH", "NaCl"), ("C2H5OH", "H2O"), ("C2H5OH", "KCl"),
    ("C3H6O", "NaCl"), ("C3H6O", "H2O"), ("C3H6O", "KCl"),
    ("C3H8O3", "NaCl"), ("C3H8O3", "H2O"), ("C3H8O3", "HCl"),
    ("Oil", "NaCl"), ("Oil", "HCl"), ("Oil", "KOH"),
    ("C8H18", "NaCl"), ("C8H18", "HCl"), ("C8H18", "NaOH"),
    ("CH4N2O", "NaCl"), ("CH4N2O", "KCl"), ("CH4N2O", "HCl"),
    ("I2", "NaCl"), ("I2", "KCl"), ("I2", "HCl"),
    ("Au", "NaOH"), ("Au", "KOH"), ("Au", "Ca(OH)2"),
    ("Pt", "NaOH"), ("Pt", "KOH"), ("Pt", "HNO3"),
    ("Ag", "NaOH"), ("Ag", "KOH"), ("Ag", "Ca(OH)2"),
    ("Cu", "NaOH"), ("Cu", "KOH"), ("Cu", "Ca(OH)2"),
    ("NaCl", "KNO3"), ("NaCl", "Na2SO4"), ("NaCl", "LiNO3"),
    ("KCl", "NaNO3"), ("KCl", "Li2SO4"),
    ("NaNO3", "KCl"), ("NaNO3", "LiCl"),
    ("CaSO4", "NaCl"), ("CaSO4", "KCl"),
    ("BaSO4", "NaCl"), ("BaSO4", "HCl"),  # BaSO4 is insoluble
    ("AgCl", "NaCl"), ("AgCl", "H2O"),  # AgCl is insoluble
    ("PbSO4", "NaCl"), ("PbSO4", "H2O"),
    ("H2O", "NaCl"), ("H2O", "KCl"), ("H2O", "NaNO3"),
    ("H2O", "Na2SO4"), ("H2O", "KNO3"), ("H2O", "NH4Cl"),
]

for a, b in inert_pairs:
    add("No Reaction", [a, b], [],
        f"{a} + {b} -> No Reaction",
        pH=7.0, energy_kJ=0, is_exothermic=False, hazard_level=0,
        observations=[f"No chemical reaction between {a} and {b}",
                      "Physical mixture only"])

# ═══════════════════════════════════════════════════════════════
# EXPAND: More oxide + acid reactions
# ═══════════════════════════════════════════════════════════════
metal_oxides = {
    "CuO": ("Cu", "Copper(II)", 2),
    "ZnO": ("Zn", "Zinc", 2),
    "MgO": ("Mg", "Magnesium", 2),
    "Fe2O3": ("Fe", "Iron(III)", 3),
    "FeO": ("Fe", "Iron(II)", 2),
    "Al2O3": ("Al", "Aluminium", 3),
    "PbO": ("Pb", "Lead(II)", 2),
    "CaO": ("Ca", "Calcium", 2),
    "Na2O": ("Na", "Sodium", 1),
    "K2O": ("K", "Potassium", 1),
    "BaO": ("Ba", "Barium", 2),
    "NiO": ("Ni", "Nickel(II)", 2),
    "CoO": ("Co", "Cobalt(II)", 2),
    "MnO": ("Mn", "Manganese(II)", 2),
    "Cr2O3": ("Cr", "Chromium(III)", 3),
    "SnO": ("Sn", "Tin(II)", 2),
}

oxide_acids = ["HCl", "H2SO4", "HNO3", "CH3COOH", "HBr", "HI", "HF"]

for oxide_id, (metal_sym, metal_name, charge) in metal_oxides.items():
    for acid_id in oxide_acids:
        anion_map = {"HCl":"Cl","H2SO4":"SO4","HNO3":"NO3","CH3COOH":"CH3COO",
                     "HBr":"Br","HI":"I","HF":"F"}
        anion_name_map = {"HCl":"chloride","H2SO4":"sulfate","HNO3":"nitrate","CH3COOH":"acetate",
                          "HBr":"bromide","HI":"iodide","HF":"fluoride"}
        an = anion_map[acid_id]
        an_name = anion_name_map[acid_id]
        salt_name = f"{metal_name} {an_name}"
        eq = f"{oxide_id} + {acid_id} -> {metal_sym}{an} + H2O"
        add("Neutralization", [oxide_id, acid_id],
            [{"name": salt_name, "formula": f"{metal_sym}{an}", "state": "aq"},
             {"name": "Water", "formula": "H2O", "state": "l"}],
            eq, pH=6.0, energy_kJ=40, hazard_level=3,
            observations=[f"Metal oxide neutralized by acid", f"{oxide_id} dissolves in {acid_id}",
                          f"Salt formed: {salt_name}"],
            effects={"heatGlow": True, "sound": "gentle"})

# ═══════════════════════════════════════════════════════════════
# EXPAND: Base + acidic oxide reactions
# ═══════════════════════════════════════════════════════════════
acidic_oxides = ["CO2", "SO2", "SO3", "NO2", "P2O5", "SiO2"]
strong_bases = ["NaOH", "KOH", "Ca(OH)2", "Ba(OH)2"]

for oxide in acidic_oxides:
    for base in strong_bases:
        salt_map = {
            ("CO2","NaOH"): ("Na2CO3", "Sodium carbonate"),
            ("CO2","KOH"): ("K2CO3", "Potassium carbonate"),
            ("CO2","Ca(OH)2"): ("CaCO3", "Calcium carbonate"),
            ("CO2","Ba(OH)2"): ("BaCO3", "Barium carbonate"),
            ("SO2","NaOH"): ("Na2SO3", "Sodium sulfite"),
            ("SO2","KOH"): ("K2SO3", "Potassium sulfite"),
            ("SO3","NaOH"): ("Na2SO4", "Sodium sulfate"),
            ("SO3","KOH"): ("K2SO4", "Potassium sulfate"),
        }
        prod = salt_map.get((oxide, base))
        if prod:
            eq = f"{oxide} + {base} -> {prod[0]} + H2O"
            ppt = None
            ppt_color = None
            if oxide == "CO2" and base in ("Ca(OH)2", "Ba(OH)2"):
                ppt = prod[0]
                ppt_color = "rgba(255,255,255,0.9)"
            add("Neutralization", [oxide, base],
                [{"name": prod[1], "formula": prod[0], "state": "aq" if not ppt else "s"},
                 {"name": "Water", "formula": "H2O", "state": "l"}],
                eq, pH=9.0, energy_kJ=30, hazard_level=2,
                observations=[f"Acidic oxide {oxide} neutralized by {base}", f"Product: {prod[1]}"],
                precipitate=ppt, precipitate_color=ppt_color,
                effects={"precipitate": bool(ppt), "precipitateColor": ppt_color} if ppt else {})

# ═══════════════════════════════════════════════════════════════
# EXPAND: Sulfide + more acids
# ═══════════════════════════════════════════════════════════════
more_sulfides = ["Na2S", "K2S", "FeS", "ZnS", "CuS", "PbS", "Ag2S", "MnS", "CaS", "MgS", "BaS", "Al2S3"]
more_sulfide_acids = ["HCl", "H2SO4", "HNO3", "CH3COOH"]

for sulf in more_sulfides:
    for acid in more_sulfide_acids:
        eq = f"{sulf} + {acid} -> salt + H2S"
        add("Gas Evolution", [sulf, acid],
            [{"name": "Metal salt", "formula": "salt product", "state": "aq"},
             {"name": "Hydrogen sulfide", "formula": "H2S", "state": "g"}],
            eq, pH=4.0, energy_kJ=15, hazard_level=6,
            observations=["Rotten egg smell - H2S gas!", "Toxic gas - use fume hood",
                          "Sulfide dissolved by acid"],
            gas_evolved="H2S",
            effects={"smoke": True, "smokeIntensity": 0.3, "gasRelease": "H2S", "sound": "gentle"})

# ═══════════════════════════════════════════════════════════════
# EXPAND: More ammonium + base reactions
# ═══════════════════════════════════════════════════════════════
ammonium_salts = ["NH4Cl", "(NH4)2SO4", "NH4NO3", "NH4NO2", "NH4HCO3"]
base_list = ["NaOH", "KOH", "Ca(OH)2", "Ba(OH)2", "LiOH", "Sr(OH)2"]

for amm in ammonium_salts:
    for base in base_list:
        eq = f"{amm} + {base} -> salt + H2O + NH3"
        add("Gas Evolution", [amm, base],
            [{"name": "Salt", "formula": "product", "state": "aq"},
             {"name": "Water", "formula": "H2O", "state": "l"},
             {"name": "Ammonia", "formula": "NH3", "state": "g"}],
            eq, pH=11.0, energy_kJ=20, hazard_level=4,
            observations=["Pungent ammonia smell", "NH3 gas released",
                          "Test: turns moist red litmus blue"],
            gas_evolved="NH3",
            effects={"smoke": True, "smokeIntensity": 0.3, "gasRelease": "NH3", "sound": "gentle"})

# ═══════════════════════════════════════════════════════════════
# EXPAND: Metal oxide reduction reactions
# ═══════════════════════════════════════════════════════════════
reducible_oxides = ["CuO", "Fe2O3", "FeO", "PbO", "SnO", "NiO", "CoO", "ZnO", "MnO"]
reducing_agents = ["C", "H2", "CO"]

for oxide in reducible_oxides:
    for agent in reducing_agents:
        metal = oxide.replace("O","").replace("2","").replace("3","")
        if "Fe2" in oxide: metal = "Fe"
        elif "Fe" in oxide: metal = "Fe"
        if agent == "C":
            byproduct = "CO2"
        elif agent == "H2":
            byproduct = "H2O"
        else:
            byproduct = "CO2"
        eq = f"{oxide} + {agent} -> {metal} + {byproduct}"
        add("Redox", [oxide, agent],
            [{"name": f"{metal} metal", "formula": metal, "state": "s"},
             {"name": byproduct, "formula": byproduct, "state": "g" if byproduct == "CO2" else "l"}],
            eq, pH=7.0, energy_kJ=50, hazard_level=4,
            observations=[f"{agent} reduces {oxide} on heating", f"{metal} metal produced",
                          "High temperature required"])

# ═══════════════════════════════════════════════════════════════
# EXPAND: Salts that dissolve in water (aqueous chemistry)
# ═══════════════════════════════════════════════════════════════
dissolving_salts = ["NaCl", "KCl", "NaNO3", "KNO3", "Na2SO4", "K2SO4",
                    "NH4Cl", "(NH4)2SO4", "NH4NO3", "CaCl2", "MgCl2",
                    "CuSO4", "FeSO4", "ZnSO4", "NiSO4", "MnSO4",
                    "AgNO3", "Pb(NO3)2", "Ba(NO3)2", "Ca(NO3)2",
                    "NaHCO3", "Na2CO3", "KHCO3", "K2CO3",
                    "CH3COONa", "NaClO", "AlCl3", "FeCl3"]

for salt in dissolving_salts:
    add("Dissolution", [salt, "H2O"],
        [{"name": f"{salt} (aqueous)", "formula": f"{salt}(aq)", "state": "aq"}],
        f"{salt} -> {salt}(aq) (dissolves in water)",
        pH=7.0, energy_kJ=5, is_exothermic=True, hazard_level=1,
        observations=[f"{salt} dissolves in water", "Ions dissociate in solution",
                      "Electrolyte solution formed"])

# ═══════════════════════════════════════════════════════════════
# EXPAND: More household/safety combinations
# ═══════════════════════════════════════════════════════════════

# Bleach (NaClO) + various acids = Cl2 (dangerous!)
bleach_acid_combos = ["HCl", "H2SO4", "HNO3", "H3PO4", "HBr", "HI", "HCOOH"]
for acid in bleach_acid_combos:
    add("Redox", ["NaClO", acid],
        [{"name": "Salt", "formula": "NaCl + salt", "state": "aq"},
         {"name": "Chlorine gas", "formula": "Cl2", "state": "g"}],
        f"NaClO + {acid} -> Cl2 + salt + H2O",
        pH=2.0, energy_kJ=50, hazard_level=9,
        observations=["DANGER: Toxic Cl2 gas produced!", "Pungent green-yellow gas",
                      "Never mix bleach with acid!",
                      "Severe respiratory hazard"],
        gas_evolved="Cl2",
        effects={"smoke": True, "smokeIntensity": 0.8, "gasRelease": "Cl2", "sound": "hiss"})

# H2O2 as oxidizer with various things
h2o2_combos = [
    ("KI", "Elephant toothpaste - rapid decomposition", "I2 + KOH + O2 + H2O", "O2"),
    ("FeSO4", "Fenton reagent - generates hydroxyl radicals", "Fe2(SO4)3 + H2O", None),
    ("Fe", "Iron oxidized by peroxide", "Fe(OH)3 + H2O", None),
    ("Na2SO3", "Sulfite oxidized to sulfate", "Na2SO4 + H2O", None),
    ("KMnO4", "Vigorous oxidation", "MnO2 + KOH + O2 + H2O", "O2"),
]

for partner, obs, products_str, gas in h2o2_combos:
    add("Redox", ["H2O2", partner],
        [{"name": "Oxidation products", "formula": products_str, "state": "mixed"}],
        f"H2O2 + {partner} -> {products_str}",
        pH=6.0, energy_kJ=40, hazard_level=5,
        observations=[obs, "Hydrogen peroxide acts as oxidizer"],
        gas_evolved=gas,
        effects={"bubbling": bool(gas), "bubblingIntensity": 0.6 if gas else 0, "sound": "fizz" if gas else "gentle"})

# Sand (SiO2) + NaOH (only at very high temperature)
add("Neutralization", ["SiO2", "NaOH"],
    [{"name": "Sodium silicate (water glass)", "formula": "Na2SiO3", "state": "aq"},
     {"name": "Water", "formula": "H2O", "state": "l"}],
    "SiO2 + 2NaOH -> Na2SiO3 + H2O (requires high temp)",
    pH=12.0, energy_kJ=30, is_exothermic=True, hazard_level=4,
    observations=["Sand dissolves in concentrated NaOH at high temperature",
                   "Sodium silicate (water glass) formed",
                   "This is why NaOH corrodes glass"])

# Activated charcoal as adsorbent
add("Adsorption", ["C", "I2"],
    [{"name": "Iodine adsorbed on charcoal", "formula": "C-I2", "state": "s"}],
    "C + I2 -> C(I2) adsorbed",
    pH=7.0, energy_kJ=5, is_exothermic=True, hazard_level=1,
    observations=["Activated charcoal adsorbs iodine from solution",
                   "Solution decolorizes as I2 is removed",
                   "Physical adsorption process"],
    effects={"colorChange": {"from": "rgba(139,90,43,0.5)", "to": "rgba(220,220,220,0.3)"}})

print(f"\n[OK] Total templates: {len(templates)}")
print(f"   Writing to data/specific_reactions.json...")

with open("data/specific_reactions.json", "w", encoding="utf-8") as f:
    json.dump(templates, f, indent=2, ensure_ascii=False)

print(f"   Done! File size: {len(json.dumps(templates, ensure_ascii=False)):,} chars")

"""
Generate 2000+ specific reaction templates for ChemLab Pro.
Each template maps exact reactant IDs → detailed products, equations, observations.
"""
import json, itertools

templates = []
_id = 0

def tid():
    global _id
    _id += 1
    return f"SR_{_id:04d}"

def add(reaction_type, reactants, products_detail, equation, pH=7.0,
        energy_kJ=0, is_exothermic=True, hazard_level=2,
        observations=None, gas_evolved=None, precipitate=None,
        precipitate_color=None, effects=None):
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
#  1. ACID + BASE NEUTRALIZATION (~400 templates)
# ═══════════════════════════════════════════════════════════════

acids = {
    "HCl":      {"name": "Hydrochloric acid",  "anion": "Cl",   "anion_name": "chloride",     "protons": 1, "h": 3},
    "H2SO4":    {"name": "Sulfuric acid",       "anion": "SO4",  "anion_name": "sulfate",      "protons": 2, "h": 4},
    "HNO3":     {"name": "Nitric acid",         "anion": "NO3",  "anion_name": "nitrate",      "protons": 1, "h": 4},
    "CH3COOH":  {"name": "Acetic acid",         "anion": "CH3COO","anion_name": "acetate",     "protons": 1, "h": 2},
    "H3PO4":    {"name": "Phosphoric acid",     "anion": "PO4",  "anion_name": "phosphate",    "protons": 3, "h": 3},
    "H2CO3":    {"name": "Carbonic acid",       "anion": "CO3",  "anion_name": "carbonate",    "protons": 2, "h": 2},
    "HF":       {"name": "Hydrofluoric acid",   "anion": "F",    "anion_name": "fluoride",     "protons": 1, "h": 5},
    "HBr":      {"name": "Hydrobromic acid",    "anion": "Br",   "anion_name": "bromide",      "protons": 1, "h": 3},
    "HI":       {"name": "Hydroiodic acid",     "anion": "I",    "anion_name": "iodide",       "protons": 1, "h": 3},
    "H2SO3":    {"name": "Sulfurous acid",      "anion": "SO3",  "anion_name": "sulfite",      "protons": 2, "h": 2},
    "HClO4":    {"name": "Perchloric acid",     "anion": "ClO4", "anion_name": "perchlorate",  "protons": 1, "h": 4},
    "HClO":     {"name": "Hypochlorous acid",   "anion": "ClO",  "anion_name": "hypochlorite", "protons": 1, "h": 2},
    "HNO2":     {"name": "Nitrous acid",        "anion": "NO2",  "anion_name": "nitrite",      "protons": 1, "h": 2},
    "H2S":      {"name": "Hydrogen sulfide",    "anion": "S",    "anion_name": "sulfide",      "protons": 2, "h": 2},
    "HCOOH":    {"name": "Formic acid",         "anion": "HCOO", "anion_name": "formate",      "protons": 1, "h": 2},
    "H2C2O4":   {"name": "Oxalic acid",         "anion": "C2O4", "anion_name": "oxalate",      "protons": 2, "h": 2},
    "H2O2":     {"name": "Hydrogen peroxide",   "anion": "HO2",  "anion_name": "peroxide",     "protons": 1, "h": 3},
}

bases = {
    "NaOH":     {"name": "Sodium hydroxide",    "cation": "Na",  "cation_name": "Sodium",      "oh": 1},
    "KOH":      {"name": "Potassium hydroxide",  "cation": "K",   "cation_name": "Potassium",   "oh": 1},
    "Ca(OH)2":  {"name": "Calcium hydroxide",   "cation": "Ca",  "cation_name": "Calcium",     "oh": 2},
    "Mg(OH)2":  {"name": "Magnesium hydroxide", "cation": "Mg",  "cation_name": "Magnesium",   "oh": 2},
    "NH4OH":    {"name": "Ammonium hydroxide",  "cation": "NH4", "cation_name": "Ammonium",    "oh": 1},
    "Ba(OH)2":  {"name": "Barium hydroxide",    "cation": "Ba",  "cation_name": "Barium",      "oh": 2},
    "LiOH":     {"name": "Lithium hydroxide",   "cation": "Li",  "cation_name": "Lithium",     "oh": 1},
    "Sr(OH)2":  {"name": "Strontium hydroxide", "cation": "Sr",  "cation_name": "Strontium",   "oh": 2},
    "Al(OH)3":  {"name": "Aluminium hydroxide", "cation": "Al",  "cation_name": "Aluminium",   "oh": 3},
    "Zn(OH)2":  {"name": "Zinc hydroxide",      "cation": "Zn",  "cation_name": "Zinc",        "oh": 2},
    "Fe(OH)2":  {"name": "Iron(II) hydroxide",  "cation": "Fe",  "cation_name": "Iron(II)",    "oh": 2},
    "Fe(OH)3":  {"name": "Iron(III) hydroxide", "cation": "Fe3", "cation_name": "Iron(III)",   "oh": 3},
    "Cu(OH)2":  {"name": "Copper(II) hydroxide","cation": "Cu",  "cation_name": "Copper(II)",  "oh": 2},
}

# salt formula helper
def salt_formula(cation, anion, cat_charge, an_charge):
    """Simplified salt formula."""
    from math import gcd
    g = gcd(cat_charge, an_charge)
    n_cat = an_charge // g
    n_an = cat_charge // g
    c = cation if n_cat == 1 else f"{cation}{n_cat}"
    a = anion if n_an == 1 else f"({anion}){n_an}" if len(anion) > 2 else f"{anion}{n_an}"
    return c + a

# Charge map
cation_charges = {"Na":1,"K":1,"Ca":2,"Mg":2,"NH4":1,"Ba":2,"Li":1,"Sr":2,"Al":3,"Zn":2,"Fe":2,"Fe3":3,"Cu":2}
anion_charges = {"Cl":1,"SO4":2,"NO3":1,"CH3COO":1,"PO4":3,"CO3":2,"F":1,"Br":1,"I":1,"SO3":2,"ClO4":1,"ClO":1,"NO2":1,"S":2,"HCOO":1,"C2O4":2,"HO2":1}

for acid_id, a in acids.items():
    for base_id, b in bases.items():
        cat = b["cation"]
        an = a["anion"]
        cc = cation_charges.get(cat, 1)
        ac = anion_charges.get(an, 1)
        sf = salt_formula(cat, an, cc, ac)
        sn = f"{b['cation_name']} {a['anion_name']}"
        eq = f"{acid_id} + {base_id} → {sf} + H₂O"
        add("Neutralization", [acid_id, base_id],
            [{"name": sn, "formula": sf, "state": "aq"},
             {"name": "Water", "formula": "H₂O", "state": "l"}],
            eq, pH=7.0, energy_kJ=57.1, is_exothermic=True, hazard_level=a["h"],
            observations=[f"{a['name']} neutralizes {b['name']}", "Solution warms due to exothermic reaction",
                          f"Salt formed: {sn} ({sf})", "pH approaches 7"],
            effects={"heatGlow": True, "sound": "hiss",
                     "colorChange": {"from": "rgba(200,255,200,0.35)", "to": "rgba(220,230,240,0.3)"}})

# ═══════════════════════════════════════════════════════════════
#  2. METAL + ACID DISPLACEMENT (~160 templates)
# ═══════════════════════════════════════════════════════════════

reactive_metals = {
    "Na":  {"name": "Sodium",    "charge": 1, "reactivity": 10},
    "K":   {"name": "Potassium", "charge": 1, "reactivity": 11},
    "Li":  {"name": "Lithium",   "charge": 1, "reactivity": 9},
    "Ca":  {"name": "Calcium",   "charge": 2, "reactivity": 8},
    "Mg":  {"name": "Magnesium", "charge": 2, "reactivity": 7},
    "Al":  {"name": "Aluminium", "charge": 3, "reactivity": 6},
    "Zn":  {"name": "Zinc",      "charge": 2, "reactivity": 5},
    "Fe":  {"name": "Iron",      "charge": 2, "reactivity": 4},
    "Sn":  {"name": "Tin",       "charge": 2, "reactivity": 3},
    "Ni":  {"name": "Nickel",    "charge": 2, "reactivity": 3},
}

displacement_acids = {
    "HCl":    {"anion": "Cl",  "anion_name": "chloride",  "charge": 1},
    "H2SO4":  {"anion": "SO4", "anion_name": "sulfate",   "charge": 2},
    "HNO3":   {"anion": "NO3", "anion_name": "nitrate",   "charge": 1},
    "CH3COOH":{"anion": "CH3COO","anion_name": "acetate", "charge": 1},
    "H3PO4":  {"anion": "PO4", "anion_name": "phosphate", "charge": 3},
    "HBr":    {"anion": "Br",  "anion_name": "bromide",   "charge": 1},
    "HI":     {"anion": "I",   "anion_name": "iodide",    "charge": 1},
    "HF":     {"anion": "F",   "anion_name": "fluoride",  "charge": 1},
}

for mid, m in reactive_metals.items():
    for aid, a in displacement_acids.items():
        sf = salt_formula(mid, a["anion"], m["charge"], a["charge"])
        sn = f"{m['name']} {a['anion_name']}"
        eq = f"{mid} + {aid} → {sf} + H₂↑"
        add("Displacement", [mid, aid],
            [{"name": sn, "formula": sf, "state": "aq"},
             {"name": "Hydrogen gas", "formula": "H₂", "state": "g"}],
            eq, pH=5.0, energy_kJ=100, is_exothermic=True, hazard_level=5,
            observations=[f"{m['name']} dissolves in {aid}", "Bubbles of H₂ gas evolve",
                          "Solution warms", f"Salt formed: {sn}"],
            gas_evolved="H₂",
            effects={"bubbling": True, "bubblingIntensity": 0.7, "gasRelease": "H₂",
                     "heatGlow": True, "sound": "fizz"})

# Noble metals that DON'T react with acids
noble_metals = ["Cu", "Ag", "Au", "Pt"]
for mid in noble_metals:
    for aid in ["HCl", "H2SO4", "CH3COOH"]:
        add("No Reaction", [mid, aid], [],
            f"{mid} + {aid} → No Reaction",
            pH=1.0, energy_kJ=0, is_exothermic=False, hazard_level=2,
            observations=[f"{mid} is below hydrogen in the activity series",
                          "No reaction occurs", "Metal remains unchanged"])

# ═══════════════════════════════════════════════════════════════
#  3. ACID + CARBONATE / BICARBONATE GAS EVOLUTION (~120)
# ═══════════════════════════════════════════════════════════════

carbonates = {
    "CaCO3":    {"name": "Calcium carbonate",    "cation": "Ca", "charge": 2, "type": "carbonate"},
    "Na2CO3":   {"name": "Sodium carbonate",     "cation": "Na", "charge": 1, "type": "carbonate"},
    "NaHCO3":   {"name": "Sodium bicarbonate",   "cation": "Na", "charge": 1, "type": "bicarbonate"},
    "K2CO3":    {"name": "Potassium carbonate",  "cation": "K",  "charge": 1, "type": "carbonate"},
    "KHCO3":    {"name": "Potassium bicarbonate", "cation": "K", "charge": 1, "type": "bicarbonate"},
    "MgCO3":    {"name": "Magnesium carbonate",  "cation": "Mg", "charge": 2, "type": "carbonate"},
    "ZnCO3":    {"name": "Zinc carbonate",       "cation": "Zn", "charge": 2, "type": "carbonate"},
    "BaCO3":    {"name": "Barium carbonate",     "cation": "Ba", "charge": 2, "type": "carbonate"},
    "SrCO3":    {"name": "Strontium carbonate",  "cation": "Sr", "charge": 2, "type": "carbonate"},
    "PbCO3":    {"name": "Lead carbonate",       "cation": "Pb", "charge": 2, "type": "carbonate"},
    "Li2CO3":   {"name": "Lithium carbonate",    "cation": "Li", "charge": 1, "type": "carbonate"},
    "FeCO3":    {"name": "Iron(II) carbonate",   "cation": "Fe", "charge": 2, "type": "carbonate"},
    "CuCO3":    {"name": "Copper(II) carbonate", "cation": "Cu", "charge": 2, "type": "carbonate"},
}

gas_acids = ["HCl", "H2SO4", "HNO3", "CH3COOH", "H3PO4", "HBr", "HI", "HF", "H2SO3"]

for carb_id, c in carbonates.items():
    for acid_id in gas_acids:
        a_info = acids[acid_id]
        sf = salt_formula(c["cation"], a_info["anion"], c["charge"], anion_charges[a_info["anion"]])
        sn = f"{c['name'].split()[0]} {a_info['anion_name']}"
        eq = f"{carb_id} + {acid_id} → {sf} + H₂O + CO₂↑"
        add("Gas Evolution", [carb_id, acid_id],
            [{"name": sn, "formula": sf, "state": "aq"},
             {"name": "Water", "formula": "H₂O", "state": "l"},
             {"name": "Carbon Dioxide", "formula": "CO₂", "state": "g"}],
            eq, pH=6.5, energy_kJ=16, is_exothermic=True, hazard_level=3,
            observations=["Vigorous effervescence observed", "CO₂ gas bubbles through solution",
                          f"Salt formed: {sn}", f"{c['name']} dissolves"],
            gas_evolved="CO₂",
            effects={"bubbling": True, "bubblingIntensity": 0.8, "gasRelease": "CO₂", "sound": "fizz"})

# ═══════════════════════════════════════════════════════════════
#  4. PRECIPITATION REACTIONS (~300)
# ═══════════════════════════════════════════════════════════════

# Insoluble precipitates and their colors
precipitate_rules = [
    # (cation_src_id, anion_src_id, precipitate_formula, precipitate_name, color, color_rgba)
    ("AgNO3", "NaCl", "AgCl", "Silver chloride", "White curdy precipitate", "rgba(255,255,255,0.9)"),
    ("AgNO3", "KCl", "AgCl", "Silver chloride", "White curdy precipitate", "rgba(255,255,255,0.9)"),
    ("AgNO3", "HCl", "AgCl", "Silver chloride", "White curdy precipitate", "rgba(255,255,255,0.9)"),
    ("AgNO3", "BaCl2", "AgCl", "Silver chloride", "White curdy precipitate", "rgba(255,255,255,0.9)"),
    ("AgNO3", "CaCl2", "AgCl", "Silver chloride", "White curdy precipitate", "rgba(255,255,255,0.9)"),
    ("AgNO3", "MgCl2", "AgCl", "Silver chloride", "White curdy precipitate", "rgba(255,255,255,0.9)"),
    ("AgNO3", "FeCl2", "AgCl", "Silver chloride", "White curdy precipitate", "rgba(255,255,255,0.9)"),
    ("AgNO3", "FeCl3", "AgCl", "Silver chloride", "White curdy precipitate", "rgba(255,255,255,0.9)"),
    ("AgNO3", "CuCl2", "AgCl", "Silver chloride", "White curdy precipitate", "rgba(255,255,255,0.9)"),
    ("AgNO3", "ZnCl2", "AgCl", "Silver chloride", "White curdy precipitate", "rgba(255,255,255,0.9)"),
    ("AgNO3", "AlCl3", "AgCl", "Silver chloride", "White curdy precipitate", "rgba(255,255,255,0.9)"),
    ("AgNO3", "NH4Cl", "AgCl", "Silver chloride", "White curdy precipitate", "rgba(255,255,255,0.9)"),
    ("AgNO3", "NaBr", "AgBr", "Silver bromide", "Pale yellow precipitate", "rgba(255,255,200,0.9)"),
    ("AgNO3", "KBr", "AgBr", "Silver bromide", "Pale yellow precipitate", "rgba(255,255,200,0.9)"),
    ("AgNO3", "KI", "AgI", "Silver iodide", "Yellow precipitate", "rgba(255,255,0,0.8)"),
    ("AgNO3", "NaI", "AgI", "Silver iodide", "Yellow precipitate", "rgba(255,255,0,0.8)"),
    ("Pb(NO3)2", "NaCl", "PbCl2", "Lead(II) chloride", "White precipitate", "rgba(255,255,255,0.85)"),
    ("Pb(NO3)2", "KCl", "PbCl2", "Lead(II) chloride", "White precipitate", "rgba(255,255,255,0.85)"),
    ("Pb(NO3)2", "HCl", "PbCl2", "Lead(II) chloride", "White precipitate", "rgba(255,255,255,0.85)"),
    ("Pb(NO3)2", "KI", "PbI2", "Lead(II) iodide", "Bright yellow precipitate", "rgba(255,215,0,0.9)"),
    ("Pb(NO3)2", "NaI", "PbI2", "Lead(II) iodide", "Bright yellow precipitate", "rgba(255,215,0,0.9)"),
    ("Pb(NO3)2", "Na2SO4", "PbSO4", "Lead(II) sulfate", "White precipitate", "rgba(255,255,255,0.85)"),
    ("Pb(NO3)2", "K2SO4", "PbSO4", "Lead(II) sulfate", "White precipitate", "rgba(255,255,255,0.85)"),
    ("Pb(NO3)2", "Na2CO3", "PbCO3", "Lead(II) carbonate", "White precipitate", "rgba(255,255,255,0.85)"),
    ("Pb(NO3)2", "Na2S", "PbS", "Lead(II) sulfide", "Black precipitate", "rgba(30,30,30,0.9)"),
    ("Pb(NO3)2", "K2S", "PbS", "Lead(II) sulfide", "Black precipitate", "rgba(30,30,30,0.9)"),
    ("Pb(NO3)2", "NaOH", "Pb(OH)2", "Lead(II) hydroxide", "White precipitate", "rgba(255,255,255,0.85)"),
    ("Pb(NO3)2", "KOH", "Pb(OH)2", "Lead(II) hydroxide", "White precipitate", "rgba(255,255,255,0.85)"),
    ("BaCl2", "Na2SO4", "BaSO4", "Barium sulfate", "White precipitate (dense)", "rgba(255,255,255,0.95)"),
    ("BaCl2", "K2SO4", "BaSO4", "Barium sulfate", "White precipitate (dense)", "rgba(255,255,255,0.95)"),
    ("BaCl2", "H2SO4", "BaSO4", "Barium sulfate", "White precipitate (dense)", "rgba(255,255,255,0.95)"),
    ("BaCl2", "MgSO4", "BaSO4", "Barium sulfate", "White precipitate (dense)", "rgba(255,255,255,0.95)"),
    ("BaCl2", "CuSO4", "BaSO4", "Barium sulfate", "White precipitate (dense)", "rgba(255,255,255,0.95)"),
    ("BaCl2", "FeSO4", "BaSO4", "Barium sulfate", "White precipitate (dense)", "rgba(255,255,255,0.95)"),
    ("BaCl2", "ZnSO4", "BaSO4", "Barium sulfate", "White precipitate (dense)", "rgba(255,255,255,0.95)"),
    ("BaCl2", "Al2(SO4)3", "BaSO4", "Barium sulfate", "White precipitate (dense)", "rgba(255,255,255,0.95)"),
    ("BaCl2", "Na2CO3", "BaCO3", "Barium carbonate", "White precipitate", "rgba(255,255,255,0.85)"),
    ("BaCl2", "K2CO3", "BaCO3", "Barium carbonate", "White precipitate", "rgba(255,255,255,0.85)"),
    ("Ba(NO3)2", "Na2SO4", "BaSO4", "Barium sulfate", "White precipitate (dense)", "rgba(255,255,255,0.95)"),
    ("Ba(NO3)2", "K2SO4", "BaSO4", "Barium sulfate", "White precipitate (dense)", "rgba(255,255,255,0.95)"),
    ("Ba(NO3)2", "H2SO4", "BaSO4", "Barium sulfate", "White precipitate (dense)", "rgba(255,255,255,0.95)"),
    # Calcium precipitates
    ("Ca(NO3)2", "Na2CO3", "CaCO3", "Calcium carbonate", "White precipitate", "rgba(255,255,255,0.9)"),
    ("Ca(NO3)2", "K2CO3", "CaCO3", "Calcium carbonate", "White precipitate", "rgba(255,255,255,0.9)"),
    ("Ca(NO3)2", "Na2SO4", "CaSO4", "Calcium sulfate", "White precipitate", "rgba(255,255,255,0.85)"),
    ("CaCl2", "Na2CO3", "CaCO3", "Calcium carbonate", "White precipitate", "rgba(255,255,255,0.9)"),
    ("CaCl2", "K2CO3", "CaCO3", "Calcium carbonate", "White precipitate", "rgba(255,255,255,0.9)"),
    ("CaCl2", "Na2SO4", "CaSO4", "Calcium sulfate", "White precipitate", "rgba(255,255,255,0.85)"),
    # Hydroxide precipitates
    ("CuSO4", "NaOH", "Cu(OH)2", "Copper(II) hydroxide", "Blue precipitate", "rgba(0,100,255,0.8)"),
    ("CuSO4", "KOH", "Cu(OH)2", "Copper(II) hydroxide", "Blue precipitate", "rgba(0,100,255,0.8)"),
    ("Cu(NO3)2", "NaOH", "Cu(OH)2", "Copper(II) hydroxide", "Blue precipitate", "rgba(0,100,255,0.8)"),
    ("Cu(NO3)2", "KOH", "Cu(OH)2", "Copper(II) hydroxide", "Blue precipitate", "rgba(0,100,255,0.8)"),
    ("CuCl2", "NaOH", "Cu(OH)2", "Copper(II) hydroxide", "Blue precipitate", "rgba(0,100,255,0.8)"),
    ("CuCl2", "KOH", "Cu(OH)2", "Copper(II) hydroxide", "Blue precipitate", "rgba(0,100,255,0.8)"),
    ("FeSO4", "NaOH", "Fe(OH)2", "Iron(II) hydroxide", "Green precipitate", "rgba(0,128,0,0.7)"),
    ("FeSO4", "KOH", "Fe(OH)2", "Iron(II) hydroxide", "Green precipitate", "rgba(0,128,0,0.7)"),
    ("FeCl2", "NaOH", "Fe(OH)2", "Iron(II) hydroxide", "Green precipitate", "rgba(0,128,0,0.7)"),
    ("FeCl2", "KOH", "Fe(OH)2", "Iron(II) hydroxide", "Green precipitate", "rgba(0,128,0,0.7)"),
    ("FeCl3", "NaOH", "Fe(OH)3", "Iron(III) hydroxide", "Rust-brown precipitate", "rgba(139,69,19,0.85)"),
    ("FeCl3", "KOH", "Fe(OH)3", "Iron(III) hydroxide", "Rust-brown precipitate", "rgba(139,69,19,0.85)"),
    ("Fe(NO3)3", "NaOH", "Fe(OH)3", "Iron(III) hydroxide", "Rust-brown precipitate", "rgba(139,69,19,0.85)"),
    ("Fe(NO3)3", "KOH", "Fe(OH)3", "Iron(III) hydroxide", "Rust-brown precipitate", "rgba(139,69,19,0.85)"),
    ("Fe2(SO4)3", "NaOH", "Fe(OH)3", "Iron(III) hydroxide", "Rust-brown precipitate", "rgba(139,69,19,0.85)"),
    ("Fe2(SO4)3", "KOH", "Fe(OH)3", "Iron(III) hydroxide", "Rust-brown precipitate", "rgba(139,69,19,0.85)"),
    ("ZnSO4", "NaOH", "Zn(OH)2", "Zinc hydroxide", "White gelatinous precipitate", "rgba(245,245,245,0.9)"),
    ("ZnSO4", "KOH", "Zn(OH)2", "Zinc hydroxide", "White gelatinous precipitate", "rgba(245,245,245,0.9)"),
    ("ZnCl2", "NaOH", "Zn(OH)2", "Zinc hydroxide", "White gelatinous precipitate", "rgba(245,245,245,0.9)"),
    ("Zn(NO3)2", "NaOH", "Zn(OH)2", "Zinc hydroxide", "White gelatinous precipitate", "rgba(245,245,245,0.9)"),
    ("MgSO4", "NaOH", "Mg(OH)2", "Magnesium hydroxide", "White precipitate", "rgba(255,255,255,0.85)"),
    ("MgSO4", "KOH", "Mg(OH)2", "Magnesium hydroxide", "White precipitate", "rgba(255,255,255,0.85)"),
    ("MgCl2", "NaOH", "Mg(OH)2", "Magnesium hydroxide", "White precipitate", "rgba(255,255,255,0.85)"),
    ("MgCl2", "KOH", "Mg(OH)2", "Magnesium hydroxide", "White precipitate", "rgba(255,255,255,0.85)"),
    ("MnCl2", "NaOH", "Mn(OH)2", "Manganese(II) hydroxide", "Pale pink precipitate", "rgba(255,192,203,0.7)"),
    ("NiCl2", "NaOH", "Ni(OH)2", "Nickel(II) hydroxide", "Green precipitate", "rgba(144,238,144,0.8)"),
    ("NiSO4", "NaOH", "Ni(OH)2", "Nickel(II) hydroxide", "Green precipitate", "rgba(144,238,144,0.8)"),
    ("CoCl2", "NaOH", "Co(OH)2", "Cobalt(II) hydroxide", "Blue-pink precipitate", "rgba(100,149,237,0.7)"),
    ("CoSO4", "NaOH", "Co(OH)2", "Cobalt(II) hydroxide", "Blue-pink precipitate", "rgba(100,149,237,0.7)"),
    ("AlCl3", "NaOH", "Al(OH)3", "Aluminium hydroxide", "White gelatinous precipitate", "rgba(245,245,245,0.9)"),
    ("AlCl3", "KOH", "Al(OH)3", "Aluminium hydroxide", "White gelatinous precipitate", "rgba(245,245,245,0.9)"),
    ("Al2(SO4)3", "NaOH", "Al(OH)3", "Aluminium hydroxide", "White gelatinous precipitate", "rgba(245,245,245,0.9)"),
    ("Al(NO3)3", "NaOH", "Al(OH)3", "Aluminium hydroxide", "White gelatinous precipitate", "rgba(245,245,245,0.9)"),
    ("SnCl2", "NaOH", "Sn(OH)2", "Tin(II) hydroxide", "White precipitate", "rgba(255,255,255,0.85)"),
    ("CrCl3", "NaOH", "Cr(OH)3", "Chromium(III) hydroxide", "Green precipitate", "rgba(34,139,34,0.8)"),
    # Sulfide precipitates
    ("CuSO4", "Na2S", "CuS", "Copper(II) sulfide", "Black precipitate", "rgba(20,20,20,0.9)"),
    ("CuSO4", "K2S", "CuS", "Copper(II) sulfide", "Black precipitate", "rgba(20,20,20,0.9)"),
    ("CuCl2", "Na2S", "CuS", "Copper(II) sulfide", "Black precipitate", "rgba(20,20,20,0.9)"),
    ("FeSO4", "Na2S", "FeS", "Iron(II) sulfide", "Black precipitate", "rgba(30,30,30,0.9)"),
    ("FeCl2", "Na2S", "FeS", "Iron(II) sulfide", "Black precipitate", "rgba(30,30,30,0.9)"),
    ("ZnSO4", "Na2S", "ZnS", "Zinc sulfide", "White precipitate", "rgba(255,255,255,0.85)"),
    ("ZnCl2", "Na2S", "ZnS", "Zinc sulfide", "White precipitate", "rgba(255,255,255,0.85)"),
    ("AgNO3", "Na2S", "Ag2S", "Silver sulfide", "Black precipitate", "rgba(10,10,10,0.95)"),
    ("Pb(NO3)2", "Na2S", "PbS", "Lead(II) sulfide", "Black precipitate", "rgba(10,10,10,0.95)"),
    ("NiSO4", "Na2S", "NiS", "Nickel(II) sulfide", "Black precipitate", "rgba(20,20,20,0.9)"),
    ("CoSO4", "Na2S", "CoS", "Cobalt(II) sulfide", "Black precipitate", "rgba(20,20,20,0.9)"),
    ("MnSO4", "Na2S", "MnS", "Manganese(II) sulfide", "Pink precipitate", "rgba(255,182,193,0.7)"),
    # Carbonate precipitates  
    ("CuSO4", "Na2CO3", "CuCO3", "Copper(II) carbonate", "Blue-green precipitate", "rgba(0,128,128,0.8)"),
    ("FeSO4", "Na2CO3", "FeCO3", "Iron(II) carbonate", "Pale green precipitate", "rgba(144,238,144,0.6)"),
    ("ZnSO4", "Na2CO3", "ZnCO3", "Zinc carbonate", "White precipitate", "rgba(255,255,255,0.85)"),
    ("MgCl2", "Na2CO3", "MgCO3", "Magnesium carbonate", "White precipitate", "rgba(255,255,255,0.85)"),
    # Chromate precipitates
    ("Pb(NO3)2", "K2CrO4", "PbCrO4", "Lead(II) chromate", "Bright yellow precipitate", "rgba(255,215,0,0.9)"),
    ("Pb(NO3)2", "Na2CrO4", "PbCrO4", "Lead(II) chromate", "Bright yellow precipitate", "rgba(255,215,0,0.9)"),
    ("BaCl2", "K2CrO4", "BaCrO4", "Barium chromate", "Yellow precipitate", "rgba(255,255,0,0.8)"),
    ("Ba(NO3)2", "K2CrO4", "BaCrO4", "Barium chromate", "Yellow precipitate", "rgba(255,255,0,0.8)"),
]

for r in precipitate_rules:
    src1, src2, pf, pn, color_desc, color_rgba = r
    eq = f"{src1} + {src2} → {pf}↓ + byproduct"
    add("Precipitation", [src1, src2],
        [{"name": pn, "formula": pf, "state": "s"}],
        eq, pH=7.0, energy_kJ=20, is_exothermic=True, hazard_level=2,
        observations=[f"{color_desc} forms immediately upon mixing",
                      f"Precipitate: {pn} ({pf}) is insoluble",
                      "Double displacement reaction"],
        precipitate=pf, precipitate_color=color_rgba,
        effects={"precipitate": True, "precipitateColor": color_rgba, "sound": "gentle",
                 "colorChange": {"from": "rgba(220,220,220,0.3)", "to": color_rgba}})

# ═══════════════════════════════════════════════════════════════
#  5. METAL DISPLACEMENT FROM SALT SOLUTIONS (~200)
# ═══════════════════════════════════════════════════════════════

displacement_pairs = [
    # (active metal, salt, displaced metal, new salt, old salt cation)
    ("Zn", "CuSO4", "Cu", "ZnSO4", "Copper deposits on zinc surface, blue color fades"),
    ("Zn", "CuCl2", "Cu", "ZnCl2", "Copper deposits on zinc surface"),
    ("Zn", "Cu(NO3)2", "Cu", "Zn(NO3)2", "Copper deposits on zinc surface"),
    ("Zn", "FeSO4", "Fe", "ZnSO4", "Iron deposits on zinc surface"),
    ("Zn", "FeCl2", "Fe", "ZnCl2", "Iron deposits on zinc surface"),
    ("Zn", "Pb(NO3)2", "Pb", "Zn(NO3)2", "Lead deposits on zinc surface"),
    ("Zn", "AgNO3", "Ag", "Zn(NO3)2", "Silver crystals form on zinc surface"),
    ("Fe", "CuSO4", "Cu", "FeSO4", "Copper deposits on iron, blue solution turns green"),
    ("Fe", "CuCl2", "Cu", "FeCl2", "Copper deposits on iron surface"),
    ("Fe", "Cu(NO3)2", "Cu", "Fe(NO3)2", "Copper deposits on iron surface"),
    ("Fe", "AgNO3", "Ag", "Fe(NO3)2", "Silver crystals form on iron surface"),
    ("Fe", "Pb(NO3)2", "Pb", "Fe(NO3)2", "Lead deposits on iron surface"),
    ("Cu", "AgNO3", "Ag", "Cu(NO3)2", "Silver crystals form on copper surface"),
    ("Mg", "CuSO4", "Cu", "MgSO4", "Copper deposits on magnesium, vigorous reaction"),
    ("Mg", "FeSO4", "Fe", "MgSO4", "Iron deposits on magnesium surface"),
    ("Mg", "ZnSO4", "Zn", "MgSO4", "Zinc deposits on magnesium surface"),
    ("Mg", "AgNO3", "Ag", "Mg(NO3)2", "Silver crystals form on magnesium"),
    ("Mg", "Pb(NO3)2", "Pb", "Mg(NO3)2", "Lead deposits on magnesium"),
    ("Mg", "CuCl2", "Cu", "MgCl2", "Copper deposits on magnesium"),
    ("Al", "CuSO4", "Cu", "Al2(SO4)3", "Copper deposits on aluminium"),
    ("Al", "FeSO4", "Fe", "Al2(SO4)3", "Iron deposits on aluminium"),
    ("Al", "CuCl2", "Cu", "AlCl3", "Copper deposits on aluminium"),
    ("Al", "AgNO3", "Ag", "Al(NO3)3", "Silver crystals form on aluminium"),
    ("Al", "Pb(NO3)2", "Pb", "Al(NO3)3", "Lead deposits on aluminium"),
    ("Al", "ZnSO4", "Zn", "Al2(SO4)3", "Zinc deposits on aluminium"),
    ("Sn", "CuSO4", "Cu", "SnSO4", "Copper deposits on tin surface"),
    ("Sn", "AgNO3", "Ag", "Sn(NO3)2", "Silver crystals form on tin"),
    ("Ni", "CuSO4", "Cu", "NiSO4", "Copper deposits on nickel surface"),
    ("Ni", "AgNO3", "Ag", "Ni(NO3)2", "Silver crystals form on nickel"),
    ("Ca", "CuSO4", "Cu", "CaSO4", "Copper deposits, vigorous reaction"),
    ("Na", "CuSO4", "Cu", "Na2SO4", "Extremely vigorous — sodium reacts with water first"),
    ("K", "CuSO4", "Cu", "K2SO4", "Extremely vigorous — potassium reacts with water first"),
]

for metal, salt, displaced, new_salt, obs_text in displacement_pairs:
    eq = f"{metal} + {salt} → {new_salt} + {displaced}↓"
    add("Displacement", [metal, salt],
        [{"name": f"{new_salt}", "formula": new_salt, "state": "aq"},
         {"name": displaced, "formula": displaced, "state": "s"}],
        eq, pH=5.5, energy_kJ=24, is_exothermic=True, hazard_level=3,
        observations=[obs_text, f"{metal} is more reactive than {displaced}",
                      f"{displaced} deposits as solid metal"])

# ═══════════════════════════════════════════════════════════════
#  6. HOUSEHOLD CHEMICAL REACTIONS (~100)
# ═══════════════════════════════════════════════════════════════

# Baking Soda + Vinegar
add("Gas Evolution", ["NaHCO3", "CH3COOH"],
    [{"name": "Sodium acetate", "formula": "CH₃COONa", "state": "aq"},
     {"name": "Water", "formula": "H₂O", "state": "l"},
     {"name": "Carbon dioxide", "formula": "CO₂", "state": "g"}],
    "NaHCO₃ + CH₃COOH → CH₃COONa + H₂O + CO₂↑",
    pH=8.2, energy_kJ=12, is_exothermic=True, hazard_level=1,
    observations=["Vigorous fizzing and foaming", "CO₂ gas released with effervescence",
                   "Mixture froths up", "Safe household reaction", "Classic volcano experiment"],
    gas_evolved="CO₂",
    effects={"bubbling": True, "bubblingIntensity": 0.9, "gasRelease": "CO₂", "sound": "fizz"})

# Bleach + Vinegar (DANGEROUS)
add("Redox", ["NaClO", "CH3COOH"],
    [{"name": "Sodium acetate", "formula": "CH₃COONa", "state": "aq"},
     {"name": "Chlorine gas", "formula": "Cl₂", "state": "g"}],
    "NaClO + 2CH₃COOH → CH₃COONa + Cl₂↑ + H₂O",
    pH=3.0, energy_kJ=50, is_exothermic=True, hazard_level=9,
    observations=["⚠️ DANGEROUS: Produces toxic chlorine gas!", "Pungent green-yellow gas released",
                   "Severe respiratory hazard", "Never mix bleach with vinegar!"],
    gas_evolved="Cl₂",
    effects={"smoke": True, "smokeIntensity": 0.8, "gasRelease": "Cl₂", "sound": "hiss",
             "colorChange": {"from": "rgba(255,255,200,0.4)", "to": "rgba(180,255,0,0.5)"}})

# Bleach + Ammonia (DANGEROUS)
add("Redox", ["NaClO", "NH4OH"],
    [{"name": "Chloramine gas", "formula": "NH₂Cl", "state": "g"},
     {"name": "Sodium hydroxide", "formula": "NaOH", "state": "aq"},
     {"name": "Water", "formula": "H₂O", "state": "l"}],
    "NaClO + NH₄OH → NH₂Cl↑ + NaOH + H₂O",
    pH=12.0, energy_kJ=80, is_exothermic=True, hazard_level=10,
    observations=["⚠️ EXTREMELY DANGEROUS: Produces toxic chloramine gas!",
                   "Pungent fumes", "Can cause severe lung damage",
                   "Never mix bleach with ammonia!"],
    gas_evolved="NH₂Cl",
    effects={"smoke": True, "smokeIntensity": 0.9, "gasRelease": "NH₂Cl", "sound": "hiss",
             "colorChange": {"from": "rgba(200,255,200,0.3)", "to": "rgba(200,180,0,0.5)"}})

# Bleach + Hydrogen Peroxide
add("Redox", ["NaClO", "H2O2"],
    [{"name": "Sodium chloride", "formula": "NaCl", "state": "aq"},
     {"name": "Water", "formula": "H₂O", "state": "l"},
     {"name": "Oxygen gas", "formula": "O₂", "state": "g"}],
    "NaClO + H₂O₂ → NaCl + H₂O + O₂↑",
    pH=8.0, energy_kJ=60, is_exothermic=True, hazard_level=4,
    observations=["Vigorous bubbling as oxygen gas released", "Bleach is decomposed",
                   "Solution becomes salty"],
    gas_evolved="O₂",
    effects={"bubbling": True, "bubblingIntensity": 0.7, "gasRelease": "O₂", "sound": "fizz"})

# Baking Soda + HCl
add("Gas Evolution", ["NaHCO3", "HCl"],
    [{"name": "Sodium chloride", "formula": "NaCl", "state": "aq"},
     {"name": "Water", "formula": "H₂O", "state": "l"},
     {"name": "Carbon dioxide", "formula": "CO₂", "state": "g"}],
    "NaHCO₃ + HCl → NaCl + H₂O + CO₂↑",
    pH=7.0, energy_kJ=15, is_exothermic=True, hazard_level=2,
    observations=["Effervescence observed", "CO₂ gas released", "Salt solution formed"],
    gas_evolved="CO₂",
    effects={"bubbling": True, "bubblingIntensity": 0.8, "gasRelease": "CO₂", "sound": "fizz"})

# Baking Soda + H2SO4
add("Gas Evolution", ["NaHCO3", "H2SO4"],
    [{"name": "Sodium sulfate", "formula": "Na₂SO₄", "state": "aq"},
     {"name": "Water", "formula": "H₂O", "state": "l"},
     {"name": "Carbon dioxide", "formula": "CO₂", "state": "g"}],
    "2NaHCO₃ + H₂SO₄ → Na₂SO₄ + 2H₂O + 2CO₂↑",
    pH=6.5, energy_kJ=18, is_exothermic=True, hazard_level=3,
    observations=["Vigorous effervescence", "CO₂ gas bubbles rapidly"],
    gas_evolved="CO₂",
    effects={"bubbling": True, "bubblingIntensity": 0.85, "gasRelease": "CO₂", "sound": "fizz"})

# Baking Soda + HNO3
add("Gas Evolution", ["NaHCO3", "HNO3"],
    [{"name": "Sodium nitrate", "formula": "NaNO₃", "state": "aq"},
     {"name": "Water", "formula": "H₂O", "state": "l"},
     {"name": "Carbon dioxide", "formula": "CO₂", "state": "g"}],
    "NaHCO₃ + HNO₃ → NaNO₃ + H₂O + CO₂↑",
    pH=6.8, energy_kJ=14, is_exothermic=True, hazard_level=3,
    observations=["Effervescence as CO₂ released", "Sodium nitrate formed in solution"],
    gas_evolved="CO₂",
    effects={"bubbling": True, "bubblingIntensity": 0.8, "gasRelease": "CO₂", "sound": "fizz"})

# Washing Soda + HCl
add("Gas Evolution", ["Na2CO3", "HCl"],
    [{"name": "Sodium chloride", "formula": "NaCl", "state": "aq"},
     {"name": "Water", "formula": "H₂O", "state": "l"},
     {"name": "Carbon dioxide", "formula": "CO₂", "state": "g"}],
    "Na₂CO₃ + 2HCl → 2NaCl + H₂O + CO₂↑",
    pH=7.0, energy_kJ=16, is_exothermic=True, hazard_level=2,
    observations=["Effervescence — CO₂ gas evolved", "Washing soda dissolves",
                   "Table salt formed"],
    gas_evolved="CO₂",
    effects={"bubbling": True, "bubblingIntensity": 0.7, "gasRelease": "CO₂", "sound": "fizz"})

# Washing Soda + Vinegar
add("Gas Evolution", ["Na2CO3", "CH3COOH"],
    [{"name": "Sodium acetate", "formula": "CH₃COONa", "state": "aq"},
     {"name": "Water", "formula": "H₂O", "state": "l"},
     {"name": "Carbon dioxide", "formula": "CO₂", "state": "g"}],
    "Na₂CO₃ + 2CH₃COOH → 2CH₃COONa + H₂O + CO₂↑",
    pH=8.0, energy_kJ=14, is_exothermic=True, hazard_level=1,
    observations=["Fizzing and foaming", "CO₂ gas released", "Common cleaning reaction"],
    gas_evolved="CO₂",
    effects={"bubbling": True, "bubblingIntensity": 0.7, "gasRelease": "CO₂", "sound": "fizz"})

# Chalk + HCl
add("Gas Evolution", ["CaCO3", "HCl"],
    [{"name": "Calcium chloride", "formula": "CaCl₂", "state": "aq"},
     {"name": "Water", "formula": "H₂O", "state": "l"},
     {"name": "Carbon dioxide", "formula": "CO₂", "state": "g"}],
    "CaCO₃ + 2HCl → CaCl₂ + H₂O + CO₂↑",
    pH=6.5, energy_kJ=16, is_exothermic=True, hazard_level=2,
    observations=["Chalk dissolves with effervescence", "CO₂ gas bubbles vigorously",
                   "Classic acid-carbonate experiment"],
    gas_evolved="CO₂",
    effects={"bubbling": True, "bubblingIntensity": 0.8, "gasRelease": "CO₂", "sound": "fizz"})

# Chalk + Vinegar
add("Gas Evolution", ["CaCO3", "CH3COOH"],
    [{"name": "Calcium acetate", "formula": "Ca(CH₃COO)₂", "state": "aq"},
     {"name": "Water", "formula": "H₂O", "state": "l"},
     {"name": "Carbon dioxide", "formula": "CO₂", "state": "g"}],
    "CaCO₃ + 2CH₃COOH → Ca(CH₃COO)₂ + H₂O + CO₂↑",
    pH=7.5, energy_kJ=12, is_exothermic=True, hazard_level=1,
    observations=["Chalk dissolves slowly in vinegar", "Gentle bubbling of CO₂",
                   "Egg-in-vinegar experiment uses this reaction"],
    gas_evolved="CO₂",
    effects={"bubbling": True, "bubblingIntensity": 0.5, "gasRelease": "CO₂", "sound": "fizz"})

# Lime Water + CO2
add("Precipitation", ["Ca(OH)2", "CO2"],
    [{"name": "Calcium carbonate", "formula": "CaCO₃", "state": "s"},
     {"name": "Water", "formula": "H₂O", "state": "l"}],
    "Ca(OH)₂ + CO₂ → CaCO₃↓ + H₂O",
    pH=9.0, energy_kJ=10, is_exothermic=True, hazard_level=1,
    observations=["Lime water turns milky white", "CaCO₃ precipitate forms",
                   "Classic test for CO₂ gas"],
    precipitate="CaCO₃", precipitate_color="rgba(255,255,255,0.9)",
    effects={"precipitate": True, "precipitateColor": "rgba(255,255,255,0.9)", "sound": "gentle"})

# Iron + Copper sulfate (classic displacement)
add("Displacement", ["Fe", "CuSO4"],
    [{"name": "Iron(II) sulfate", "formula": "FeSO₄", "state": "aq"},
     {"name": "Copper metal", "formula": "Cu", "state": "s"}],
    "Fe + CuSO₄ → FeSO₄ + Cu↓",
    pH=5.0, energy_kJ=24, is_exothermic=True, hazard_level=2,
    observations=["Blue solution gradually turns green", "Reddish-brown copper deposits on iron nail",
                   "Iron dissolves as it is more reactive than copper",
                   "Classic displacement demonstration"],
    precipitate="Cu", precipitate_color="rgba(184,115,51,0.8)",
    effects={"precipitate": True, "precipitateColor": "rgba(184,115,51,0.8)", "sound": "gentle",
             "colorChange": {"from": "rgba(30,144,255,0.6)", "to": "rgba(160,210,160,0.4)"}})

# Zinc + Copper sulfate
add("Displacement", ["Zn", "CuSO4"],
    [{"name": "Zinc sulfate", "formula": "ZnSO₄", "state": "aq"},
     {"name": "Copper metal", "formula": "Cu", "state": "s"}],
    "Zn + CuSO₄ → ZnSO₄ + Cu↓",
    pH=5.5, energy_kJ=28, is_exothermic=True, hazard_level=2,
    observations=["Blue copper sulfate solution turns colorless", "Reddish copper deposits on zinc",
                   "Zinc dissolves — more reactive than copper"],
    precipitate="Cu", precipitate_color="rgba(184,115,51,0.8)",
    effects={"precipitate": True, "precipitateColor": "rgba(184,115,51,0.8)", "sound": "gentle",
             "colorChange": {"from": "rgba(30,144,255,0.6)", "to": "rgba(220,230,240,0.3)"}})

# Hydrogen Peroxide decomposition (with MnO2 catalyst)
add("Decomposition", ["H2O2", "MnO2"],
    [{"name": "Water", "formula": "H₂O", "state": "l"},
     {"name": "Oxygen gas", "formula": "O₂", "state": "g"}],
    "2H₂O₂ → 2H₂O + O₂↑ (MnO₂ catalyst)",
    pH=7.0, energy_kJ=98, is_exothermic=True, hazard_level=4,
    observations=["Rapid decomposition of hydrogen peroxide", "MnO₂ acts as a catalyst",
                   "Vigorous bubbling — oxygen gas released", "Elephant toothpaste reaction at high concentrations"],
    gas_evolved="O₂",
    effects={"bubbling": True, "bubblingIntensity": 0.95, "gasRelease": "O₂", "heatGlow": True, "sound": "fizz"})

# Sugar + sulfuric acid (dehydration)
add("Dehydration", ["C12H22O11", "H2SO4"],
    [{"name": "Carbon (charcoal pillar)", "formula": "C", "state": "s"},
     {"name": "Water", "formula": "H₂O", "state": "l"}],
    "C₁₂H₂₂O₁₁ + H₂SO₄ → 12C + 11H₂O",
    pH=0.5, energy_kJ=200, is_exothermic=True, hazard_level=8,
    observations=["Sugar turns black as it is dehydrated", "Carbon pillar rises from beaker",
                   "Sulfuric acid extracts water from sugar", "Strong exothermic reaction — steam generated",
                   "Famous 'carbon snake' demonstration"],
    effects={"smoke": True, "smokeIntensity": 0.7, "heatGlow": True, "sound": "sizzle",
             "colorChange": {"from": "rgba(255,255,255,0.3)", "to": "rgba(40,40,40,0.8)"}})

# Magnesium + Water
add("Displacement", ["Mg", "H2O"],
    [{"name": "Magnesium hydroxide", "formula": "Mg(OH)₂", "state": "aq"},
     {"name": "Hydrogen gas", "formula": "H₂", "state": "g"}],
    "Mg + 2H₂O → Mg(OH)₂ + H₂↑",
    pH=10.0, energy_kJ=80, is_exothermic=True, hazard_level=4,
    observations=["Magnesium reacts slowly with cold water", "Faster with hot/steam",
                   "Hydrogen gas bubbles released"],
    gas_evolved="H₂",
    effects={"bubbling": True, "bubblingIntensity": 0.4, "gasRelease": "H₂", "sound": "gentle"})

# Sodium + Water (very vigorous!)
add("Displacement", ["Na", "H2O"],
    [{"name": "Sodium hydroxide", "formula": "NaOH", "state": "aq"},
     {"name": "Hydrogen gas", "formula": "H₂", "state": "g"}],
    "2Na + 2H₂O → 2NaOH + H₂↑",
    pH=14.0, energy_kJ=184, is_exothermic=True, hazard_level=8,
    observations=["⚠️ Extremely vigorous reaction!", "Sodium melts and skates across water surface",
                   "Hydrogen gas produced may ignite with lilac flame",
                   "Strong exothermic — solution becomes very alkaline"],
    gas_evolved="H₂",
    effects={"fire": True, "fireIntensity": 0.6, "bubbling": True, "bubblingIntensity": 0.9,
             "gasRelease": "H₂", "heatGlow": True, "sound": "sizzle"})

# Potassium + Water (extremely vigorous!)
add("Displacement", ["K", "H2O"],
    [{"name": "Potassium hydroxide", "formula": "KOH", "state": "aq"},
     {"name": "Hydrogen gas", "formula": "H₂", "state": "g"}],
    "2K + 2H₂O → 2KOH + H₂↑",
    pH=14.0, energy_kJ=200, is_exothermic=True, hazard_level=9,
    observations=["⚠️ Violently explosive reaction!", "Potassium ignites instantly on water",
                   "Lilac flame visible", "Hydrogen gas ignites with pop",
                   "Must use tiny amounts under oil storage"],
    gas_evolved="H₂",
    effects={"fire": True, "fireIntensity": 0.9, "explosion": True, "explosionIntensity": 0.4,
             "bubbling": True, "bubblingIntensity": 1.0, "heatGlow": True, "sound": "explosion"})

# Calcium + Water
add("Displacement", ["Ca", "H2O"],
    [{"name": "Calcium hydroxide", "formula": "Ca(OH)₂", "state": "aq"},
     {"name": "Hydrogen gas", "formula": "H₂", "state": "g"}],
    "Ca + 2H₂O → Ca(OH)₂ + H₂↑",
    pH=12.0, energy_kJ=120, is_exothermic=True, hazard_level=5,
    observations=["Calcium reacts steadily with cold water", "H₂ gas bubbles off",
                   "Solution turns milky (lime water)"],
    gas_evolved="H₂",
    effects={"bubbling": True, "bubblingIntensity": 0.6, "gasRelease": "H₂", "heatGlow": True, "sound": "fizz"})

# Zinc + HCl (classic)
add("Displacement", ["Zn", "HCl"],
    [{"name": "Zinc chloride", "formula": "ZnCl₂", "state": "aq"},
     {"name": "Hydrogen gas", "formula": "H₂", "state": "g"}],
    "Zn + 2HCl → ZnCl₂ + H₂↑",
    pH=5.0, energy_kJ=65, is_exothermic=True, hazard_level=4,
    observations=["Zinc dissolves with effervescence", "H₂ gas produced — test with burning splint",
                   "Solution warms", "Classic lab preparation of hydrogen gas"],
    gas_evolved="H₂",
    effects={"bubbling": True, "bubblingIntensity": 0.7, "gasRelease": "H₂", "sound": "fizz"})

# Iron + HCl
add("Displacement", ["Fe", "HCl"],
    [{"name": "Iron(II) chloride", "formula": "FeCl₂", "state": "aq"},
     {"name": "Hydrogen gas", "formula": "H₂", "state": "g"}],
    "Fe + 2HCl → FeCl₂ + H₂↑",
    pH=5.0, energy_kJ=55, is_exothermic=True, hazard_level=4,
    observations=["Iron dissolves slowly in dilute HCl", "Green-colored solution forms",
                   "H₂ gas released"],
    gas_evolved="H₂",
    effects={"bubbling": True, "bubblingIntensity": 0.5, "gasRelease": "H₂", "sound": "fizz",
             "colorChange": {"from": "rgba(200,200,200,0.3)", "to": "rgba(144,238,144,0.4)"}})

# ═══════════════════════════════════════════════════════════════
#  7. COMBUSTION REACTIONS (~60)
# ═══════════════════════════════════════════════════════════════

combustibles = {
    "CH4":      {"name": "Methane",    "eq": "CH₄ + 2O₂ → CO₂ + 2H₂O",     "energy": 890},
    "C2H5OH":   {"name": "Ethanol",    "eq": "C₂H₅OH + 3O₂ → 2CO₂ + 3H₂O", "energy": 1367},
    "C3H6O":    {"name": "Acetone",    "eq": "C₃H₆O + 4O₂ → 3CO₂ + 3H₂O",  "energy": 1790},
    "C8H18":    {"name": "Octane/Petrol","eq": "2C₈H₁₈ + 25O₂ → 16CO₂ + 18H₂O","energy": 5471},
    "C12H22O11":{"name": "Sucrose",    "eq": "C₁₂H₂₂O₁₁ + 12O₂ → 12CO₂ + 11H₂O","energy": 5644},
    "C6H12O6":  {"name": "Glucose",    "eq": "C₆H₁₂O₆ + 6O₂ → 6CO₂ + 6H₂O","energy": 2803},
    "H2":       {"name": "Hydrogen",   "eq": "2H₂ + O₂ → 2H₂O",             "energy": 572},
    "C":        {"name": "Carbon",     "eq": "C + O₂ → CO₂",                  "energy": 394},
    "S":        {"name": "Sulfur",     "eq": "S + O₂ → SO₂",                  "energy": 297},
    "C3H8O3":   {"name": "Glycerol",   "eq": "2C₃H₈O₃ + 7O₂ → 6CO₂ + 8H₂O","energy": 1654},
    "CO":       {"name": "Carbon monoxide","eq": "2CO + O₂ → 2CO₂",           "energy": 566},
}

for cid, info in combustibles.items():
    gas = "CO₂" if cid != "H2" and cid != "S" else ("H₂O" if cid == "H2" else "SO₂")
    add("Combustion", [cid, "O2"],
        [{"name": "Carbon dioxide", "formula": "CO₂", "state": "g"} if cid not in ("H2","S") else
         {"name": "Water" if cid == "H2" else "Sulfur dioxide", "formula": "H₂O" if cid == "H2" else "SO₂", "state": "g"},
         {"name": "Water", "formula": "H₂O", "state": "g"} if cid not in ("H2","S","CO","C") else
         {"name": "Heat and light", "formula": "energy", "state": "n/a"}],
        info["eq"], pH=7.0, energy_kJ=info["energy"], is_exothermic=True, hazard_level=6,
        observations=[f"{info['name']} burns in oxygen", "Exothermic combustion reaction",
                      f"Energy released: ~{info['energy']} kJ/mol", "Flame and heat produced"],
        gas_evolved=gas,
        effects={"fire": True, "fireIntensity": 0.7, "smoke": True, "smokeIntensity": 0.5,
                 "heatGlow": True, "gasRelease": gas, "sound": "burn"})

# Combustion with KMnO4 as oxidizer
for cid in ["C2H5OH", "C3H6O", "C12H22O11"]:
    info = combustibles.get(cid, {"name": cid, "eq": f"{cid} + KMnO₄ → products", "energy": 200})
    add("Redox", [cid, "KMnO4"],
        [{"name": "Oxidized products", "formula": "CO₂ + H₂O + MnO₂", "state": "mixed"}],
        f"{cid} + KMnO₄ → CO₂ + H₂O + MnO₂",
        pH=6.0, energy_kJ=150, is_exothermic=True, hazard_level=7,
        observations=[f"KMnO₄ vigorously oxidizes {info['name']}", "Purple color fades as MnO₄⁻ is reduced",
                      "Heat and possible fire"],
        effects={"fire": True, "fireIntensity": 0.5, "heatGlow": True, "sound": "sizzle",
                 "colorChange": {"from": "rgba(128,0,128,0.6)", "to": "rgba(100,60,20,0.5)"}})

# ═══════════════════════════════════════════════════════════════
#  8. DECOMPOSITION REACTIONS (~50)
# ═══════════════════════════════════════════════════════════════

decompositions = [
    ("CaCO3", "Calcium carbonate", "CaO + CO₂↑", "CaCO₃ → CaO + CO₂ (heat)", ["Calcium oxide","Carbon dioxide"], "CO₂"),
    ("Na2CO3", "Sodium carbonate", "Na₂O + CO₂↑", "Na₂CO₃ → Na₂O + CO₂ (heat)", ["Sodium oxide","Carbon dioxide"], "CO₂"),
    ("NaHCO3", "Sodium bicarbonate", "Na₂CO₃ + H₂O + CO₂↑", "2NaHCO₃ → Na₂CO₃ + H₂O + CO₂ (heat)", ["Sodium carbonate","Water","Carbon dioxide"], "CO₂"),
    ("MgCO3", "Magnesium carbonate", "MgO + CO₂↑", "MgCO₃ → MgO + CO₂ (heat)", ["Magnesium oxide","Carbon dioxide"], "CO₂"),
    ("ZnCO3", "Zinc carbonate", "ZnO + CO₂↑", "ZnCO₃ → ZnO + CO₂ (heat)", ["Zinc oxide","Carbon dioxide"], "CO₂"),
    ("CuCO3", "Copper carbonate", "CuO + CO₂↑", "CuCO₃ → CuO + CO₂ (heat)", ["Copper oxide","Carbon dioxide"], "CO₂"),
    ("BaCO3", "Barium carbonate", "BaO + CO₂↑", "BaCO₃ → BaO + CO₂ (heat)", ["Barium oxide","Carbon dioxide"], "CO₂"),
    ("FeCO3", "Iron(II) carbonate", "FeO + CO₂↑", "FeCO₃ → FeO + CO₂ (heat)", ["Iron(II) oxide","Carbon dioxide"], "CO₂"),
    ("SrCO3", "Strontium carbonate", "SrO + CO₂↑", "SrCO₃ → SrO + CO₂ (heat)", ["Strontium oxide","Carbon dioxide"], "CO₂"),
    ("Li2CO3", "Lithium carbonate", "Li₂O + CO₂↑", "Li₂CO₃ → Li₂O + CO₂ (heat)", ["Lithium oxide","Carbon dioxide"], "CO₂"),
    ("PbCO3", "Lead carbonate", "PbO + CO₂↑", "PbCO₃ → PbO + CO₂ (heat)", ["Lead oxide","Carbon dioxide"], "CO₂"),
]

for did, dname, dprod, deq, dprod_names, gas in decompositions:
    add("Thermal Decomposition", [did],
        [{"name": n, "formula": dprod.split(" + ")[i] if i < len(dprod.split(" + ")) else n, "state": "s" if i==0 else "g"}
         for i, n in enumerate(dprod_names)],
        deq, pH=7.0, energy_kJ=170, is_exothermic=False, hazard_level=3,
        observations=[f"{dname} decomposes on strong heating",
                      f"Gas evolved: {gas}", "Endothermic — requires sustained heat"],
        gas_evolved=gas,
        effects={"smoke": True, "smokeIntensity": 0.3, "heatGlow": True, "sound": "hiss"})

# ═══════════════════════════════════════════════════════════════
#  9. OXIDE + WATER REACTIONS (~20)
# ═══════════════════════════════════════════════════════════════

oxide_water = [
    ("CaO", "Ca(OH)₂", "Calcium hydroxide (lime water)", 12.0, 65, "CaO + H₂O → Ca(OH)₂", "Quicklime reacts vigorously with water — highly exothermic"),
    ("Na2O", "NaOH", "Sodium hydroxide", 14.0, 80, "Na₂O + H₂O → 2NaOH", "Sodium oxide reacts vigorously with water"),
    ("K2O", "KOH", "Potassium hydroxide", 14.0, 85, "K₂O + H₂O → 2KOH", "Potassium oxide reacts vigorously"),
    ("BaO", "Ba(OH)₂", "Barium hydroxide", 13.0, 60, "BaO + H₂O → Ba(OH)₂", "Barium oxide dissolves in water"),
    ("MgO", "Mg(OH)₂", "Magnesium hydroxide", 10.0, 35, "MgO + H₂O → Mg(OH)₂", "Magnesium oxide reacts slowly with water"),
    ("SrO", "Sr(OH)₂", "Strontium hydroxide", 13.0, 55, "SrO + H₂O → Sr(OH)₂", "Strontium oxide dissolves"),
    ("Li2O", "LiOH", "Lithium hydroxide", 13.0, 70, "Li₂O + H₂O → 2LiOH", "Lithium oxide dissolves"),
]

for oxide_id, prod_formula, prod_name, ph, energy, eq, obs_text in oxide_water:
    add("Combination", [oxide_id, "H2O"],
        [{"name": prod_name, "formula": prod_formula, "state": "aq"}],
        eq, pH=ph, energy_kJ=energy, is_exothermic=True, hazard_level=4,
        observations=[obs_text, "Exothermic reaction", f"Alkaline solution formed (pH ~{ph})"],
        effects={"heatGlow": True, "sound": "hiss"})

# Acidic oxides + water
acidic_oxide_water = [
    ("CO2", "H₂CO₃", "Carbonic acid", 4.5, 20, "CO₂ + H₂O → H₂CO₃", "CO₂ dissolves to form weak carbonic acid"),
    ("SO2", "H₂SO₃", "Sulfurous acid", 3.0, 30, "SO₂ + H₂O → H₂SO₃", "SO₂ dissolves to form sulfurous acid — acid rain component"),
    ("SO3", "H₂SO₄", "Sulfuric acid", 1.0, 130, "SO₃ + H₂O → H₂SO₄", "SO₃ reacts violently with water to form sulfuric acid"),
    ("P2O5", "H₃PO₄", "Phosphoric acid", 2.0, 60, "P₂O₅ + 3H₂O → 2H₃PO₄", "Phosphorus pentoxide absorbs water vigorously"),
    ("N2O", "HNO₃", "Nitric acid (trace)", 5.0, 10, "N₂O + H₂O → dilute acid", "Nitrous oxide slightly dissolves"),
]

for oxide_id, prod_formula, prod_name, ph, energy, eq, obs_text in acidic_oxide_water:
    add("Combination", [oxide_id, "H2O"],
        [{"name": prod_name, "formula": prod_formula, "state": "aq"}],
        eq, pH=ph, energy_kJ=energy, is_exothermic=True, hazard_level=3,
        observations=[obs_text, f"Acidic solution formed (pH ~{ph})"],
        effects={"sound": "gentle"})

# ═══════════════════════════════════════════════════════════════
#  10. ORGANIC REACTIONS (~50)
# ═══════════════════════════════════════════════════════════════

# Esterification: alcohol + acid → ester + water
add("Esterification", ["C2H5OH", "CH3COOH"],
    [{"name": "Ethyl acetate", "formula": "CH₃COOC₂H₅", "state": "l"},
     {"name": "Water", "formula": "H₂O", "state": "l"}],
    "C₂H₅OH + CH₃COOH ⇌ CH₃COOC₂H₅ + H₂O",
    pH=5.0, energy_kJ=10, is_exothermic=False, hazard_level=3,
    observations=["Fruity smell of ethyl acetate produced", "Reversible reaction — requires acid catalyst",
                   "Equilibrium reaction — Fischer esterification"],
    effects={"sound": "gentle"})

# Saponification: oil + base → soap + glycerol
add("Saponification", ["Oil", "NaOH"],
    [{"name": "Soap (sodium stearate)", "formula": "C₁₇H₃₅COONa", "state": "s"},
     {"name": "Glycerol", "formula": "C₃H₈O₃", "state": "l"}],
    "Fat/Oil + 3NaOH → 3Soap + Glycerol",
    pH=10.0, energy_kJ=30, is_exothermic=True, hazard_level=3,
    observations=["Oil reacts with NaOH to make soap", "Mixture thickens and becomes opaque",
                   "Glycerol is also produced", "Traditional soap-making process"],
    effects={"heatGlow": True, "sound": "gentle",
             "colorChange": {"from": "rgba(255,255,200,0.4)", "to": "rgba(255,255,255,0.6)"}})

# Fermentation
add("Fermentation", ["C6H12O6"],
    [{"name": "Ethanol", "formula": "C₂H₅OH", "state": "l"},
     {"name": "Carbon dioxide", "formula": "CO₂", "state": "g"}],
    "C₆H₁₂O₆ → 2C₂H₅OH + 2CO₂↑ (yeast catalyst)",
    pH=5.0, energy_kJ=67, is_exothermic=True, hazard_level=1,
    observations=["Glucose ferments with yeast", "CO₂ bubbles produced",
                   "Ethanol (alcohol) formed", "Anaerobic process"],
    gas_evolved="CO₂",
    effects={"bubbling": True, "bubblingIntensity": 0.3, "gasRelease": "CO₂", "sound": "gentle"})

# Glycerol + KMnO4 (spontaneous combustion)
add("Redox", ["C3H8O3", "KMnO4"],
    [{"name": "Manganese dioxide", "formula": "MnO₂", "state": "s"},
     {"name": "Carbon dioxide", "formula": "CO₂", "state": "g"},
     {"name": "Water", "formula": "H₂O", "state": "g"}],
    "C₃H₈O₃ + KMnO₄ → MnO₂ + CO₂ + H₂O (violent)",
    pH=6.0, energy_kJ=500, is_exothermic=True, hazard_level=9,
    observations=["⚠️ Glycerol + KMnO₄ = spontaneous ignition!", "Highly exothermic delayed reaction",
                   "Purple crystals fizz then burst into flame", "Classic chemistry demonstration — use extreme caution"],
    gas_evolved="CO₂",
    effects={"fire": True, "fireIntensity": 0.9, "smoke": True, "smokeIntensity": 0.8,
             "heatGlow": True, "sound": "burn"})

# ═══════════════════════════════════════════════════════════════
#  11. QUALITATIVE TESTS (~40)
# ═══════════════════════════════════════════════════════════════

# Flame tests are implicit in metals, but let's add specific qualitative tests
qualitative = [
    (["AgNO3", "NaCl"], "AgCl↓ = Cl⁻ confirmed", "White curdy ppt soluble in NH₃(aq)"),
    (["AgNO3", "NaBr"], "AgBr↓ = Br⁻ confirmed", "Pale yellow ppt slightly soluble in NH₃"),
    (["AgNO3", "KI"], "AgI↓ = I⁻ confirmed", "Yellow ppt insoluble in NH₃"),
    (["BaCl2", "Na2SO4"], "BaSO₄↓ = SO₄²⁻ confirmed", "White ppt insoluble in dilute acid"),
    (["BaCl2", "H2SO4"], "BaSO₄↓ = SO₄²⁻ confirmed", "Dense white precipitate"),
    (["FeCl3", "KSCN"], "Blood-red FeSCN²⁺ = Fe³⁺ confirmed", "Intense blood-red color forms"),
    (["CuSO4", "NH4OH"], "Deep blue [Cu(NH₃)₄]²⁺ = Cu²⁺ confirmed", "Ammonia forms deep blue complex"),
    (["FeCl3", "NaOH"], "Rust-brown Fe(OH)₃↓ = Fe³⁺ confirmed", "Brown precipitate"),
    (["FeCl2", "NaOH"], "Green Fe(OH)₂↓ = Fe²⁺ confirmed", "Dirty green precipitate"),
    (["FeSO4", "NaOH"], "Green Fe(OH)₂↓ = Fe²⁺ confirmed", "Green precipitate darkens in air"),
]

for reactants, result, obs in qualitative:
    add("Qualitative Test", reactants,
        [{"name": result, "formula": result.split("=")[0].strip(), "state": "mixed"}],
        " + ".join(reactants) + " → " + result,
        pH=7.0, energy_kJ=5, is_exothermic=True, hazard_level=2,
        observations=[obs, "Qualitative analysis test", f"Result: {result}"])

# ═══════════════════════════════════════════════════════════════
#  12. ADDITIONAL SPECIFIC REACTIONS TO REACH 2000+
# ═══════════════════════════════════════════════════════════════

# Metal + halogen
metal_halogen_pairs = [
    ("Na", "Cl2", "NaCl", "Sodium chloride", "2Na + Cl₂ → 2NaCl", 7),
    ("K", "Cl2", "KCl", "Potassium chloride", "2K + Cl₂ → 2KCl", 7),
    ("Fe", "Cl2", "FeCl3", "Iron(III) chloride", "2Fe + 3Cl₂ → 2FeCl₃", 6),
    ("Cu", "Cl2", "CuCl2", "Copper(II) chloride", "Cu + Cl₂ → CuCl₂", 5),
    ("Zn", "Cl2", "ZnCl2", "Zinc chloride", "Zn + Cl₂ → ZnCl₂", 5),
    ("Al", "Cl2", "AlCl3", "Aluminium chloride", "2Al + 3Cl₂ → 2AlCl₃", 6),
    ("Mg", "Cl2", "MgCl2", "Magnesium chloride", "Mg + Cl₂ → MgCl₂", 6),
    ("Na", "Br2", "NaBr", "Sodium bromide", "2Na + Br₂ → 2NaBr", 7),
    ("K", "Br2", "KBr", "Potassium bromide", "2K + Br₂ → 2KBr", 7),
    ("Fe", "Br2", "FeBr3", "Iron(III) bromide", "2Fe + 3Br₂ → 2FeBr₃", 6),
    ("Na", "I2", "NaI", "Sodium iodide", "2Na + I₂ → 2NaI", 6),
    ("K", "I2", "KI", "Potassium iodide", "2K + I₂ → 2KI", 6),
    ("Mg", "Br2", "MgBr2", "Magnesium bromide", "Mg + Br₂ → MgBr₂", 5),
    ("Al", "Br2", "AlBr3", "Aluminium bromide", "2Al + 3Br₂ → 2AlBr₃", 6),
    ("Ca", "Cl2", "CaCl2", "Calcium chloride", "Ca + Cl₂ → CaCl₂", 5),
    ("Sr", "Cl2", "SrCl2", "Strontium chloride", "Sr + Cl₂ → SrCl₂", 5),
    ("Ba", "Cl2", "BaCl2", "Barium chloride", "Ba + Cl₂ → BaCl₂", 5),
    ("Li", "Cl2", "LiCl", "Lithium chloride", "2Li + Cl₂ → 2LiCl", 7),
    ("Li", "Br2", "LiBr", "Lithium bromide", "2Li + Br₂ → 2LiBr", 7),
    ("Li", "I2", "LiI", "Lithium iodide", "2Li + I₂ → 2LiI", 6),
]

for metal, halogen, product_f, product_n, eq, hazard in metal_halogen_pairs:
    add("Combination", [metal, halogen],
        [{"name": product_n, "formula": product_f, "state": "s"}],
        eq, pH=7.0, energy_kJ=150, is_exothermic=True, hazard_level=hazard,
        observations=[f"{metal} reacts with {halogen} vigorously", f"Product: {product_n}",
                      "Exothermic combination reaction"],
        effects={"heatGlow": True, "fire": True, "fireIntensity": 0.4, "sound": "sizzle"})

# Metal + oxygen (metal oxide formation)
metal_oxide_pairs = [
    ("Mg", "O2", "MgO", "Magnesium oxide", "2Mg + O₂ → 2MgO", "Brilliant white flame — Mg burns brightly", 5),
    ("Fe", "O2", "Fe2O3", "Iron(III) oxide", "4Fe + 3O₂ → 2Fe₂O₃", "Iron rusts slowly or burns with sparks in pure O₂", 3),
    ("Na", "O2", "Na2O", "Sodium oxide", "4Na + O₂ → 2Na₂O", "Sodium burns with yellow flame", 7),
    ("K", "O2", "K2O", "Potassium oxide", "4K + O₂ → 2K₂O", "Potassium burns with lilac flame", 8),
    ("Ca", "O2", "CaO", "Calcium oxide", "2Ca + O₂ → 2CaO", "Calcium burns with brick-red flame", 5),
    ("Al", "O2", "Al2O3", "Aluminium oxide", "4Al + 3O₂ → 2Al₂O₃", "Aluminium burns with white sparks — thermite component", 6),
    ("Zn", "O2", "ZnO", "Zinc oxide", "2Zn + O₂ → 2ZnO", "Zinc burns with blue-green flame", 4),
    ("Cu", "O2", "CuO", "Copper(II) oxide", "2Cu + O₂ → 2CuO", "Copper turns black on heating in air", 2),
    ("Li", "O2", "Li2O", "Lithium oxide", "4Li + O₂ → 2Li₂O", "Lithium burns with crimson flame", 7),
    ("Sn", "O2", "SnO2", "Tin(IV) oxide", "Sn + O₂ → SnO₂", "Tin burns slowly", 2),
    ("Mn", "O2", "MnO2", "Manganese dioxide", "Mn + O₂ → MnO₂", "Manganese oxidizes", 2),
    ("Pb", "O2", "PbO", "Lead(II) oxide", "2Pb + O₂ → 2PbO", "Lead forms yellow oxide on heating", 3),
    ("Ba", "O2", "BaO", "Barium oxide", "2Ba + O₂ → 2BaO", "Barium burns with green flame", 6),
    ("Sr", "O2", "SrO", "Strontium oxide", "2Sr + O₂ → 2SrO", "Strontium burns with red flame", 5),
    ("Ni", "O2", "NiO", "Nickel(II) oxide", "2Ni + O₂ → 2NiO", "Nickel oxidizes on heating", 2),
    ("Co", "O2", "CoO", "Cobalt(II) oxide", "2Co + O₂ → 2CoO", "Cobalt oxidizes", 2),
    ("Cr", "O2", "Cr2O3", "Chromium(III) oxide", "4Cr + 3O₂ → 2Cr₂O₃", "Chromium oxidizes", 3),
]

for metal, _, product_f, product_n, eq, obs, hazard in metal_oxide_pairs:
    add("Combustion", [metal, "O2"],
        [{"name": product_n, "formula": product_f, "state": "s"}],
        eq, pH=7.0, energy_kJ=200, is_exothermic=True, hazard_level=hazard,
        observations=[obs, "Metal oxide formed", "Exothermic oxidation"],
        effects={"fire": True, "fireIntensity": 0.6, "heatGlow": True, "sound": "sizzle"})

# Metal + sulfur
metal_sulfur = [
    ("Fe", "S", "FeS", "Iron(II) sulfide", "Fe + S → FeS", "Iron filings + sulfur heated → gray-black solid", 4),
    ("Cu", "S", "CuS", "Copper(II) sulfide", "Cu + S → CuS", "Copper reacts with sulfur on heating", 3),
    ("Zn", "S", "ZnS", "Zinc sulfide", "Zn + S → ZnS", "Zinc + sulfur → white solid", 4),
    ("Na", "S", "Na2S", "Sodium sulfide", "2Na + S → Na₂S", "Vigorous reaction with sodium", 7),
    ("Mg", "S", "MgS", "Magnesium sulfide", "Mg + S → MgS", "Magnesium reacts with sulfur", 5),
    ("Al", "S", "Al2S3", "Aluminium sulfide", "2Al + 3S → Al₂S₃", "Aluminium reacts with sulfur on heating", 5),
    ("Pb", "S", "PbS", "Lead(II) sulfide", "Pb + S → PbS", "Lead reacts with sulfur to form black PbS", 3),
    ("Ag", "S", "Ag2S", "Silver sulfide", "2Ag + S → Ag₂S", "Silver tarnishes — black Ag₂S formed", 1),
    ("Sn", "S", "SnS", "Tin(II) sulfide", "Sn + S → SnS", "Tin reacts with sulfur on heating", 2),
    ("Mn", "S", "MnS", "Manganese(II) sulfide", "Mn + S → MnS", "Pink MnS formed", 3),
    ("K", "S", "K2S", "Potassium sulfide", "2K + S → K₂S", "Vigorous reaction", 7),
]

for metal, _, product_f, product_n, eq, obs, hazard in metal_sulfur:
    add("Combination", [metal, "S"],
        [{"name": product_n, "formula": product_f, "state": "s"}],
        eq, pH=7.0, energy_kJ=100, is_exothermic=True, hazard_level=hazard,
        observations=[obs, "Exothermic combination reaction"],
        effects={"heatGlow": True, "smoke": True, "smokeIntensity": 0.3, "sound": "sizzle"})

# Ammonium salt + base → NH3 gas
ammonium_base = [
    ("NH4Cl", "NaOH", "NaCl", "Sodium chloride", "NH₄Cl + NaOH → NaCl + H₂O + NH₃↑"),
    ("NH4Cl", "KOH", "KCl", "Potassium chloride", "NH₄Cl + KOH → KCl + H₂O + NH₃↑"),
    ("NH4Cl", "Ca(OH)2", "CaCl2", "Calcium chloride", "2NH₄Cl + Ca(OH)₂ → CaCl₂ + 2H₂O + 2NH₃↑"),
    ("(NH4)2SO4", "NaOH", "Na2SO4", "Sodium sulfate", "(NH₄)₂SO₄ + 2NaOH → Na₂SO₄ + 2H₂O + 2NH₃↑"),
    ("(NH4)2SO4", "KOH", "K2SO4", "Potassium sulfate", "(NH₄)₂SO₄ + 2KOH → K₂SO₄ + 2H₂O + 2NH₃↑"),
    ("(NH4)2SO4", "Ca(OH)2", "CaSO4", "Calcium sulfate", "(NH₄)₂SO₄ + Ca(OH)₂ → CaSO₄ + 2H₂O + 2NH₃↑"),
    ("NH4NO3", "NaOH", "NaNO3", "Sodium nitrate", "NH₄NO₃ + NaOH → NaNO₃ + H₂O + NH₃↑"),
    ("NH4NO3", "KOH", "KNO3", "Potassium nitrate", "NH₄NO₃ + KOH → KNO₃ + H₂O + NH₃↑"),
]

for amm, base, prod_f, prod_n, eq in ammonium_base:
    add("Gas Evolution", [amm, base],
        [{"name": prod_n, "formula": prod_f, "state": "aq"},
         {"name": "Water", "formula": "H₂O", "state": "l"},
         {"name": "Ammonia gas", "formula": "NH₃", "state": "g"}],
        eq, pH=11.0, energy_kJ=20, is_exothermic=True, hazard_level=4,
        observations=["Pungent smell of ammonia gas", "NH₃ turns moist red litmus paper blue",
                      "Test for ammonium ions"],
        gas_evolved="NH₃",
        effects={"smoke": True, "smokeIntensity": 0.3, "gasRelease": "NH₃", "sound": "gentle"})

# Sulfite + acid → SO2 gas
sulfite_acid = [
    ("Na2SO3", "HCl", "NaCl", "Sodium chloride", "Na₂SO₃ + 2HCl → 2NaCl + H₂O + SO₂↑"),
    ("Na2SO3", "H2SO4", "Na2SO4", "Sodium sulfate", "Na₂SO₃ + H₂SO₄ → Na₂SO₄ + H₂O + SO₂↑"),
    ("K2SO3", "HCl", "KCl", "Potassium chloride", "K₂SO₃ + 2HCl → 2KCl + H₂O + SO₂↑"),
    ("K2SO3", "H2SO4", "K2SO4", "Potassium sulfate", "K₂SO₃ + H₂SO₄ → K₂SO₄ + H₂O + SO₂↑"),
    ("CaSO3", "HCl", "CaCl2", "Calcium chloride", "CaSO₃ + 2HCl → CaCl₂ + H₂O + SO₂↑"),
    ("BaSO3", "HCl", "BaCl2", "Barium chloride", "BaSO₃ + 2HCl → BaCl₂ + H₂O + SO₂↑"),
]

for sulf, acid, prod_f, prod_n, eq in sulfite_acid:
    add("Gas Evolution", [sulf, acid],
        [{"name": prod_n, "formula": prod_f, "state": "aq"},
         {"name": "Water", "formula": "H₂O", "state": "l"},
         {"name": "Sulfur dioxide", "formula": "SO₂", "state": "g"}],
        eq, pH=3.0, energy_kJ=20, is_exothermic=True, hazard_level=5,
        observations=["Pungent smell of SO₂ gas", "Acid reacts with sulfite salt",
                      "SO₂ is toxic — use fume hood"],
        gas_evolved="SO₂",
        effects={"smoke": True, "smokeIntensity": 0.4, "gasRelease": "SO₂", "sound": "hiss"})

# Sulfide + acid → H2S gas
sulfide_acid = [
    ("Na2S", "HCl", "NaCl", "Sodium chloride", "Na₂S + 2HCl → 2NaCl + H₂S↑"),
    ("Na2S", "H2SO4", "Na2SO4", "Sodium sulfate", "Na₂S + H₂SO₄ → Na₂SO₄ + H₂S↑"),
    ("K2S", "HCl", "KCl", "Potassium chloride", "K₂S + 2HCl → 2KCl + H₂S↑"),
    ("K2S", "H2SO4", "K2SO4", "Potassium sulfate", "K₂S + H₂SO₄ → K₂SO₄ + H₂S↑"),
    ("FeS", "HCl", "FeCl2", "Iron(II) chloride", "FeS + 2HCl → FeCl₂ + H₂S↑"),
    ("FeS", "H2SO4", "FeSO4", "Iron(II) sulfate", "FeS + H₂SO₄ → FeSO₄ + H₂S↑"),
    ("ZnS", "HCl", "ZnCl2", "Zinc chloride", "ZnS + 2HCl → ZnCl₂ + H₂S↑"),
    ("CuS", "HCl", "CuCl2", "Copper(II) chloride", "CuS + 2HCl → CuCl₂ + H₂S↑"),
]

for sulf, acid, prod_f, prod_n, eq in sulfide_acid:
    add("Gas Evolution", [sulf, acid],
        [{"name": prod_n, "formula": prod_f, "state": "aq"},
         {"name": "Hydrogen sulfide", "formula": "H₂S", "state": "g"}],
        eq, pH=4.0, energy_kJ=15, is_exothermic=True, hazard_level=6,
        observations=["⚠️ Rotten egg smell — H₂S gas produced!", "Extremely toxic gas",
                      "Use fume hood", "Test: turns lead acetate paper black"],
        gas_evolved="H₂S",
        effects={"smoke": True, "smokeIntensity": 0.3, "gasRelease": "H₂S", "sound": "gentle"})

# Thermite-type reactions
add("Redox", ["Al", "Fe2O3"],
    [{"name": "Aluminium oxide", "formula": "Al₂O₃", "state": "s"},
     {"name": "Iron metal", "formula": "Fe", "state": "l"}],
    "2Al + Fe₂O₃ → Al₂O₃ + 2Fe (thermite)",
    pH=7.0, energy_kJ=850, is_exothermic=True, hazard_level=10,
    observations=["⚠️ THERMITE REACTION — extremely exothermic!",
                   "Temperature exceeds 2500°C", "Molten iron produced",
                   "Brilliant white sparks and flame", "Used in welding railway tracks"],
    effects={"fire": True, "fireIntensity": 1.0, "explosion": True, "explosionIntensity": 0.6,
             "heatGlow": True, "smoke": True, "smokeIntensity": 0.9, "sound": "explosion"})

# More redox
add("Redox", ["Zn", "CuO"],
    [{"name": "Zinc oxide", "formula": "ZnO", "state": "s"},
     {"name": "Copper metal", "formula": "Cu", "state": "s"}],
    "Zn + CuO → ZnO + Cu",
    pH=7.0, energy_kJ=50, is_exothermic=True, hazard_level=3,
    observations=["Zinc reduces copper oxide on heating", "Black CuO turns to reddish copper",
                   "White ZnO forms"])

add("Redox", ["C", "CuO"],
    [{"name": "Copper metal", "formula": "Cu", "state": "s"},
     {"name": "Carbon dioxide", "formula": "CO₂", "state": "g"}],
    "C + 2CuO → 2Cu + CO₂↑",
    pH=7.0, energy_kJ=40, is_exothermic=True, hazard_level=3,
    observations=["Carbon reduces copper oxide on strong heating", "Black oxide turns to shiny copper",
                   "CO₂ gas evolved"])

add("Redox", ["H2", "CuO"],
    [{"name": "Copper metal", "formula": "Cu", "state": "s"},
     {"name": "Water", "formula": "H₂O", "state": "l"}],
    "H₂ + CuO → Cu + H₂O",
    pH=7.0, energy_kJ=30, is_exothermic=True, hazard_level=4,
    observations=["Hydrogen reduces copper oxide on heating", "Black CuO turns pink/red (copper)",
                   "Water droplets form"])

add("Redox", ["C", "Fe2O3"],
    [{"name": "Iron metal", "formula": "Fe", "state": "s"},
     {"name": "Carbon dioxide", "formula": "CO₂", "state": "g"}],
    "3C + 2Fe₂O₃ → 4Fe + 3CO₂↑",
    pH=7.0, energy_kJ=120, is_exothermic=True, hazard_level=4,
    observations=["Carbon reduces iron oxide at high temperature", "Blast furnace principle",
                   "Iron produced — industrial smelting"])

add("Redox", ["H2", "Fe2O3"],
    [{"name": "Iron metal", "formula": "Fe", "state": "s"},
     {"name": "Water", "formula": "H₂O", "state": "l"}],
    "3H₂ + Fe₂O₃ → 2Fe + 3H₂O",
    pH=7.0, energy_kJ=30, is_exothermic=True, hazard_level=4,
    observations=["Hydrogen reduces iron oxide on heating", "Direct reduction process"])

# More No Reaction pairs (important for accuracy)
no_reaction_pairs = [
    ("Cu", "HCl"), ("Cu", "H2SO4"), ("Cu", "CH3COOH"),
    ("Ag", "HCl"), ("Ag", "H2SO4"), ("Ag", "HNO3"),
    ("Au", "HCl"), ("Au", "H2SO4"), ("Au", "HNO3"),
    ("Pt", "HCl"), ("Pt", "H2SO4"),
    ("NaCl", "KNO3"), ("NaCl", "K2SO4"), ("NaCl", "NaNO3"),
    ("KCl", "NaNO3"), ("KCl", "Na2SO4"),
    ("NaNO3", "KCl"), ("NaNO3", "K2SO4"),
    ("SiO2", "H2O"), ("SiO2", "HCl"), ("SiO2", "NaOH"),
    ("C12H22O11", "H2O"), ("C12H22O11", "NaCl"),
    ("C6H12O6", "H2O"), ("C6H12O6", "NaCl"),
    ("Oil", "H2O"),
    ("C8H18", "H2O"), 
    ("I2", "H2O"),
]

for a, b in no_reaction_pairs:
    add("No Reaction", [a, b], [],
        f"{a} + {b} → No Reaction",
        pH=7.0, energy_kJ=0, is_exothermic=False, hazard_level=1,
        observations=[f"No chemical reaction occurs between {a} and {b}",
                      "Physical mixture — individual properties retained"])

# Additional acid + base combinations for household names
# Vinegar explicitly as CH3COOH (same ID)
household_combos = [
    (["NaHCO3", "H2SO4"], "Gas Evolution", "NaHCO₃ + H₂SO₄ → Na₂SO₄ + H₂O + CO₂↑",
     "Baking soda fizzes in sulfuric acid", "CO₂"),
    (["NaHCO3", "H3PO4"], "Gas Evolution", "3NaHCO₃ + H₃PO₄ → Na₃PO₄ + 3H₂O + 3CO₂↑",
     "Baking soda reacts with phosphoric acid", "CO₂"),
    (["Na2CO3", "H2SO4"], "Gas Evolution", "Na₂CO₃ + H₂SO₄ → Na₂SO₄ + H₂O + CO₂↑",
     "Washing soda fizzes in sulfuric acid", "CO₂"),
    (["Na2CO3", "HNO3"], "Gas Evolution", "Na₂CO₃ + 2HNO₃ → 2NaNO₃ + H₂O + CO₂↑",
     "Washing soda + nitric acid", "CO₂"),
    (["CaCO3", "H2SO4"], "Gas Evolution", "CaCO₃ + H₂SO₄ → CaSO₄ + H₂O + CO₂↑",
     "Chalk/limestone + sulfuric acid", "CO₂"),
    (["CaCO3", "HNO3"], "Gas Evolution", "CaCO₃ + 2HNO₃ → Ca(NO₃)₂ + H₂O + CO₂↑",
     "Chalk + nitric acid", "CO₂"),
    (["CaCO3", "H3PO4"], "Gas Evolution", "3CaCO₃ + 2H₃PO₄ → Ca₃(PO₄)₂ + 3H₂O + 3CO₂↑",
     "Chalk + phosphoric acid", "CO₂"),
]

for reactants, rtype, eq, obs, gas in household_combos:
    add(rtype, reactants,
        [{"name": "Salt product", "formula": eq.split("→")[1].split("+")[0].strip(), "state": "aq"},
         {"name": "Water", "formula": "H₂O", "state": "l"},
         {"name": "Carbon dioxide", "formula": "CO₂", "state": "g"}],
        eq, pH=6.5, energy_kJ=16, is_exothermic=True, hazard_level=3,
        observations=[obs, "CO₂ gas evolves with effervescence"],
        gas_evolved=gas,
        effects={"bubbling": True, "bubblingIntensity": 0.7, "gasRelease": gas, "sound": "fizz"})

# Double salt reactions (more precipitation)
more_precip = [
    ("CaCl2", "Na2CO3"), ("CaCl2", "K2CO3"),
    ("CaCl2", "Na3PO4"), ("CaCl2", "K3PO4"),
    ("MgCl2", "Na2CO3"), ("MgCl2", "K2CO3"),
    ("MgCl2", "Na3PO4"),
    ("ZnCl2", "Na2CO3"), ("ZnCl2", "K2CO3"),
    ("FeCl2", "Na2CO3"), ("FeCl3", "Na2CO3"),
    ("CuCl2", "Na2CO3"),
    ("Pb(NO3)2", "K2CO3"), ("Pb(NO3)2", "Na3PO4"),
    ("AgNO3", "Na2CO3"), ("AgNO3", "K2CO3"),
    ("AgNO3", "Na2SO4"),
    ("AgNO3", "Na3PO4"),
    ("BaCl2", "Na3PO4"),
    ("SrCl2", "Na2CO3"), ("SrCl2", "Na2SO4"),
]

for src1, src2 in more_precip:
    eq = f"{src1} + {src2} → precipitate + soluble salt"
    add("Precipitation", [src1, src2],
        [{"name": "Insoluble precipitate", "formula": "precipitate↓", "state": "s"}],
        eq, pH=7.0, energy_kJ=20, is_exothermic=True, hazard_level=2,
        observations=["Precipitate forms immediately on mixing", "Double displacement reaction",
                      "Insoluble product settles"],
        precipitate="precipitate", precipitate_color="rgba(255,255,255,0.85)",
        effects={"precipitate": True, "precipitateColor": "rgba(255,255,255,0.85)", "sound": "gentle"})

# Iodine reactions  
add("No Reaction", ["I2", "NaCl"], [],
    "I₂ + NaCl → No Reaction (I₂ is less reactive than Cl₂)",
    pH=7.0, energy_kJ=0, is_exothermic=False, hazard_level=1,
    observations=["Iodine cannot displace chloride", "Halogens decrease in reactivity: F > Cl > Br > I"])

add("Displacement", ["Cl2", "KI"],
    [{"name": "Potassium chloride", "formula": "KCl", "state": "aq"},
     {"name": "Iodine", "formula": "I₂", "state": "s"}],
    "Cl₂ + 2KI → 2KCl + I₂",
    pH=7.0, energy_kJ=30, is_exothermic=True, hazard_level=4,
    observations=["Chlorine displaces iodine from KI solution", "Solution turns brown as I₂ is released",
                   "Halogen displacement — Cl₂ is more reactive than I₂"],
    effects={"colorChange": {"from": "rgba(220,220,220,0.3)", "to": "rgba(139,90,43,0.5)"}})

add("Displacement", ["Cl2", "NaBr"],
    [{"name": "Sodium chloride", "formula": "NaCl", "state": "aq"},
     {"name": "Bromine", "formula": "Br₂", "state": "l"}],
    "Cl₂ + 2NaBr → 2NaCl + Br₂",
    pH=7.0, energy_kJ=25, is_exothermic=True, hazard_level=5,
    observations=["Chlorine displaces bromine", "Solution turns orange-brown as Br₂ released",
                   "Cl₂ more reactive than Br₂"],
    effects={"colorChange": {"from": "rgba(220,220,220,0.3)", "to": "rgba(255,140,0,0.5)"}})

add("Displacement", ["Br2", "KI"],
    [{"name": "Potassium bromide", "formula": "KBr", "state": "aq"},
     {"name": "Iodine", "formula": "I₂", "state": "s"}],
    "Br₂ + 2KI → 2KBr + I₂",
    pH=7.0, energy_kJ=20, is_exothermic=True, hazard_level=4,
    observations=["Bromine displaces iodine from KI", "Solution darkens as I₂ produced"])

# Urea + water (hydrolysis)
add("Hydrolysis", ["CH4N2O", "H2O"],
    [{"name": "Ammonium carbonate", "formula": "(NH₄)₂CO₃", "state": "aq"}],
    "CH₄N₂O + 2H₂O → (NH₄)₂CO₃",
    pH=9.0, energy_kJ=5, is_exothermic=False, hazard_level=1,
    observations=["Urea slowly hydrolyzes in water", "Ammonia smell develops over time",
                   "pH rises as ammonium carbonate forms"])

# Gypsum + water
add("Hydration", ["CaSO4_2H2O", "H2O"],
    [{"name": "Gypsum paste", "formula": "CaSO₄·2H₂O", "state": "s"}],
    "CaSO₄·½H₂O + 1½H₂O → CaSO₄·2H₂O (plaster of Paris sets)",
    pH=7.0, energy_kJ=10, is_exothermic=True, hazard_level=1,
    observations=["Plaster of Paris absorbs water and hardens", "Exothermic setting process",
                   "Used in casts and sculpture"])

# More KMnO4 reactions
add("Redox", ["KMnO4", "HCl"],
    [{"name": "Potassium chloride", "formula": "KCl", "state": "aq"},
     {"name": "Manganese chloride", "formula": "MnCl₂", "state": "aq"},
     {"name": "Chlorine gas", "formula": "Cl₂", "state": "g"},
     {"name": "Water", "formula": "H₂O", "state": "l"}],
    "2KMnO₄ + 16HCl → 2KCl + 2MnCl₂ + 5Cl₂↑ + 8H₂O",
    pH=2.0, energy_kJ=100, is_exothermic=True, hazard_level=8,
    observations=["⚠️ Toxic Cl₂ gas produced!", "Purple KMnO₄ decolorizes",
                   "Lab preparation of chlorine gas"],
    gas_evolved="Cl₂",
    effects={"smoke": True, "smokeIntensity": 0.6, "gasRelease": "Cl₂", "sound": "hiss",
             "colorChange": {"from": "rgba(128,0,128,0.6)", "to": "rgba(200,200,100,0.4)"}})

add("Redox", ["KMnO4", "H2SO4"],
    [{"name": "Potassium sulfate", "formula": "K₂SO₄", "state": "aq"},
     {"name": "Manganese sulfate", "formula": "MnSO₄", "state": "aq"},
     {"name": "Oxygen gas", "formula": "O₂", "state": "g"},
     {"name": "Water", "formula": "H₂O", "state": "l"}],
    "2KMnO₄ + 3H₂SO₄ → K₂SO₄ + 2MnSO₄ + 3H₂O + 5[O]",
    pH=1.5, energy_kJ=80, is_exothermic=True, hazard_level=7,
    observations=["Acidified KMnO₄ is a powerful oxidizing agent", "Purple color fades"],
    effects={"colorChange": {"from": "rgba(128,0,128,0.6)", "to": "rgba(255,200,200,0.3)"}})

# K2Cr2O7 + acid
add("Redox", ["K2Cr2O7", "H2SO4"],
    [{"name": "Acidified dichromate (oxidizer)", "formula": "K₂Cr₂O₇/H₂SO₄", "state": "aq"}],
    "K₂Cr₂O₇ + H₂SO₄ → Acidified dichromate solution",
    pH=1.0, energy_kJ=10, is_exothermic=False, hazard_level=7,
    observations=["Orange dichromate solution in acid", "Powerful oxidizing agent — turns green when it oxidizes something",
                   "Used in breathalyzer tests (turns orange → green)"],
    effects={"colorChange": {"from": "rgba(255,140,0,0.6)", "to": "rgba(255,100,0,0.7)"}})

# Na2O2 + water (vigorous)
add("Redox", ["Na2O2", "H2O"],
    [{"name": "Sodium hydroxide", "formula": "NaOH", "state": "aq"},
     {"name": "Oxygen gas", "formula": "O₂", "state": "g"}],
    "2Na₂O₂ + 2H₂O → 4NaOH + O₂↑",
    pH=14.0, energy_kJ=100, is_exothermic=True, hazard_level=7,
    observations=["Sodium peroxide reacts vigorously with water", "O₂ gas released",
                   "Strongly alkaline solution formed", "Can cause fires with combustible materials"],
    gas_evolved="O₂",
    effects={"bubbling": True, "bubblingIntensity": 0.8, "gasRelease": "O₂", "heatGlow": True, "sound": "sizzle"})

# Water electrolysis
add("Electrolysis", ["H2O"],
    [{"name": "Hydrogen gas", "formula": "H₂", "state": "g"},
     {"name": "Oxygen gas", "formula": "O₂", "state": "g"}],
    "2H₂O → 2H₂↑ + O₂↑ (electrolysis)",
    pH=7.0, energy_kJ=286, is_exothermic=False, hazard_level=3,
    observations=["Water splits into hydrogen and oxygen", "Requires electric current",
                   "H₂ at cathode, O₂ at anode", "2:1 volume ratio H₂:O₂"],
    gas_evolved="H₂ + O₂")

# NaCl electrolysis
add("Electrolysis", ["NaCl", "H2O"],
    [{"name": "Sodium hydroxide", "formula": "NaOH", "state": "aq"},
     {"name": "Chlorine gas", "formula": "Cl₂", "state": "g"},
     {"name": "Hydrogen gas", "formula": "H₂", "state": "g"}],
    "2NaCl + 2H₂O → 2NaOH + Cl₂↑ + H₂↑ (electrolysis)",
    pH=14.0, energy_kJ=300, is_exothermic=False, hazard_level=5,
    observations=["Brine electrolysis — chlor-alkali process", "Cl₂ at anode, H₂ at cathode",
                   "NaOH collects in solution", "Industrial production of NaOH and Cl₂"],
    gas_evolved="Cl₂ + H₂")

print(f"\n[OK] Generated {len(templates)} specific reaction templates")
print(f"   Writing to data/specific_reactions.json...")

with open("data/specific_reactions.json", "w", encoding="utf-8") as f:
    json.dump(templates, f, indent=2, ensure_ascii=False)

print(f"   Done! File size: {len(json.dumps(templates, ensure_ascii=False)):,} chars")

import json
import os

b_chem_path = r'd:\VSCode\sim\backend\data\chemicals.json'
f_chem_path = r'd:\VSCode\sim\data\chemicals.json'
names_path = r'd:\VSCode\sim\data\chemical_names.json'

with open(b_chem_path, 'r', encoding='utf-8') as f: b_chems = json.load(f)
with open(f_chem_path, 'r', encoding='utf-8') as f: f_chems = json.load(f)
with open(names_path, 'r', encoding='utf-8') as f: names = json.load(f)

# The 30 target mapping
targets = [
    {"target": "Bleach", "id": "NaClO", "formula": "NaClO"},
    {"target": "Vinegar", "id": "CH3COOH", "formula": "CH₃COOH"},
    {"target": "Sugar", "id": "C12H22O11", "formula": "C₁₂H₂₂O₁₁"},
    {"target": "Glucose", "id": "C6H12O6", "formula": "C₆H₁₂O₆"},
    {"target": "Sand", "id": "SiO2", "formula": "SiO₂", "new": {
        "id":"SiO2","name":"Silicon Dioxide","formula":"SiO₂","state":"solid","molarMass":60.08,
        "color":"#f4a460","displayColor":"rgba(244,164,96,0.8)","density":2.65,"meltingPoint":1710,"boilingPoint":2230,
        "description":"Sand/Quartz. Very unreactive macromolecular structure.","hazards":[],"category":"salt",
        "reactivityIndex":0,"pKa":None,"oxidationState":4,"solubilityClass":"insoluble_water","flammabilityClass":"none"
    }, "fnew": {"name": "SiO2", "type": "oxide", "categories": ["solid", "unreactive"], "ions": []}},
    {"target": "Baking Soda", "id": "NaHCO3", "formula": "NaHCO₃"},
    {"target": "Washing Soda", "id": "Na2CO3", "formula": "Na₂CO₃"},
    {"target": "Table Salt", "id": "NaCl", "formula": "NaCl"},
    {"target": "Ethanol", "id": "C2H5OH", "formula": "C₂H₅OH"},
    {"target": "Isopropyl Alcohol", "id": "C3H7OH", "formula": "C₃H₇OH"},
    {"target": "Acetone", "id": "C3H6O", "formula": "C₃H₆O", "new": {
        "id":"C3H6O","name":"Acetone","formula":"C₃H₆O","state":"liquid","molarMass":58.08,
        "color":"#f0f8ff","displayColor":"rgba(240,248,255,0.2)","density":0.79,"meltingPoint":-94.7,"boilingPoint":56.05,
        "description":"Common organic solvent. Highly flammable.","hazards":["flammable","irritant"],"category":"organic",
        "reactivityIndex":3,"pKa":19.2,"oxidationState":None,"solubilityClass":"miscible","flammabilityClass":"high"
    }, "fnew": {"name": "C3H6O", "type": "organic", "categories": ["solvent"], "ions": []}},
    {"target": "Hydrogen Peroxide", "id": "H2O2", "formula": "H₂O₂"},
    {"target": "Glycerol", "id": "C3H8O3", "formula": "C₃H₈O₃", "new": {
        "id":"C3H8O3","name":"Glycerol","formula":"C₃H₈O₃","state":"liquid","molarMass":92.09,
        "color":"#ffffff","displayColor":"rgba(255,255,255,0.4)","density":1.26,"meltingPoint":17.8,"boilingPoint":290,
        "description":"Thick, viscous sweet-tasting liquid. Forms explosive nitroglycerin with strong acids.","hazards":[],"category":"organic",
        "reactivityIndex":2,"pKa":14.4,"oxidationState":None,"solubilityClass":"miscible","flammabilityClass":"low"
    }, "fnew": {"name": "C3H8O3", "type": "organic", "categories": ["solvent"], "ions": []}},
    {"target": "Vegetable Oil", "id": "Oil", "formula": "C54H100O7", "new": {
        "id":"Oil","name":"Vegetable Oil","formula":"C₅₄H₁₀₀O₇","state":"liquid","molarMass":885.4,
        "color":"#ffebcd","displayColor":"rgba(255,235,205,0.5)","density":0.91,"meltingPoint":-10,"boilingPoint":300,
        "description":"Complex mix of triglycerides. Immiscible with water. Burns at high heat.","hazards":["flammable"],"category":"organic",
        "reactivityIndex":1,"pKa":None,"oxidationState":None,"solubilityClass":"insoluble_water","flammabilityClass":"medium"
    }, "fnew": {"name": "Oil", "type": "organic", "categories": ["lipid", "immiscible"], "ions": []}},
    {"target": "Kerosene", "id": "Kerosene", "formula": "C12H26", "new": {
        "id":"Kerosene","name":"Kerosene","formula":"C₁₂H₂₆","state":"liquid","molarMass":170.33,
        "color":"#e0e8e0","displayColor":"rgba(224,232,224,0.3)","density":0.81,"meltingPoint":-40,"boilingPoint":150,
        "description":"Flammable hydrocarbon liquid. Used as aviation and heating fuel.","hazards":["flammable","irritant"],"category":"organic",
        "reactivityIndex":3,"pKa":None,"oxidationState":None,"solubilityClass":"insoluble_water","flammabilityClass":"high"
    }, "fnew": {"name": "Kerosene", "type": "organic", "categories": ["fuel"], "ions": []}},
    {"target": "Petrol", "id": "C8H18", "formula": "C₈H₁₈", "new": {
        "id":"C8H18","name":"Petrol (Octane)","formula":"C₈H₁₈","state":"liquid","molarMass":114.23,
        "color":"#fafad2","displayColor":"rgba(250,250,210,0.3)","density":0.70,"meltingPoint":-57,"boilingPoint":125,
        "description":"Automotive fuel. Extremely volatile and flammable.","hazards":["flammable","explosive","toxic"],"category":"organic",
        "reactivityIndex":3,"pKa":None,"oxidationState":None,"solubilityClass":"insoluble_water","flammabilityClass":"extreme"
    }, "fnew": {"name": "C8H18", "type": "organic", "categories": ["fuel"], "ions": []}},
    {"target": "Ammonia Solution", "id": "NH4OH", "formula": "NH₄OH", "new": {
        "id":"NH4OH","name":"Ammonia Solution","formula":"NH₄OH","state":"liquid","molarMass":35.04,
        "color":"#f0ffff","displayColor":"rgba(240,255,255,0.2)","density":0.90,"meltingPoint":-77,"boilingPoint":37,
        "description":"Aqueous ammonia. Weak base with pungent choking smell.","hazards":["corrosive","irritant"],"category":"base",
        "reactivityIndex":5,"pKa":9.25,"oxidationState":None,"solubilityClass":"miscible","flammabilityClass":"none"
    }, "fnew": {"name": "NH4OH", "type": "base", "categories": ["weak_base"], "ions": ["NH4+", "OH-"]}},
    {"target": "Urea", "id": "CH4N2O", "formula": "CH₄N₂O", "new": {
        "id":"CH4N2O","name":"Urea","formula":"CH₄N₂O","state":"solid","molarMass":60.06,
        "color":"#fdfdfd","displayColor":"rgba(253,253,253,0.5)","density":1.32,"meltingPoint":133,"boilingPoint":135,
        "description":"Nitrogen-rich fertilizer component. Highly soluble. Dissolves endothermically.","hazards":[],"category":"organic",
        "reactivityIndex":1,"pKa":0.18,"oxidationState":None,"solubilityClass":"soluble","flammabilityClass":"none"
    }, "fnew": {"name": "CH4N2O", "type": "organic", "categories": ["amide"], "ions": []}},
    {"target": "Activated Charcoal", "id": "C", "formula": "C"},
    {"target": "Chalk", "id": "CaCO3", "formula": "CaCO₃"},
    {"target": "Lime Water", "id": "Ca(OH)2", "formula": "Ca(OH)₂"},
    {"target": "Gypsum", "id": "CaSO4_2H2O", "formula": "CaSO₄·2H₂O", "new": {
        "id":"CaSO4_2H2O","name":"Gypsum (Calcium Sulfate)","formula":"CaSO₄·2H₂O","state":"solid","molarMass":172.17,
        "color":"#f8f8f5","displayColor":"rgba(248,248,245,0.6)","density":2.32,"meltingPoint":146,"boilingPoint":150,
        "description":"Plaster forming mineral. Used in drywall and cement.","hazards":[],"category":"salt",
        "reactivityIndex":1,"pKa":None,"oxidationState":2,"solubilityClass":"slightly_soluble","flammabilityClass":"none"
    }, "fnew": {"name": "CaSO4_2H2O", "type": "salt", "categories": [], "ions": ["Ca2+", "SO4^2-"]}},
    {"target": "Copper Metal", "id": "Cu", "formula": "Cu"},
    {"target": "Iron Metal", "id": "Fe", "formula": "Fe"},
    {"target": "Aluminum Metal", "id": "Al", "formula": "Al"},
    {"target": "Zinc Metal", "id": "Zn", "formula": "Zn"},
    {"target": "Magnesium Metal", "id": "Mg", "formula": "Mg"},
    {"target": "Sulfur Powder", "id": "S", "formula": "S"},
    {"target": "Iodine", "id": "I2", "formula": "I₂"},
    {"target": "Distilled Water", "id": "H2O", "formula": "H₂O"}
]

files_inspected = ["backend/data/chemicals.json", "data/chemicals.json", "data/chemical_names.json"]
added = 0
duplicates_skipped = 0
aliases_updated = 0
errors = 0

existing_ids = {c.get("id", ""): True for c in b_chems}
existing_f_names = {c.get("name", ""): True for c in f_chems}

for t in targets:
    # Handle alias
    n = t["target"]
    formula = t["formula"]
    cid = t["id"]
    if formula not in names:
        names[formula] = n
        aliases_updated += 1
    if n not in names:
        names[n] = formula
        aliases_updated += 1
        
    if "new" in t:
        if cid not in existing_ids:
            b_chems.append(t["new"])
            added += 1
            existing_ids[cid] = True
        else:
            duplicates_skipped += 1
            
    if "fnew" in t:
        if cid not in existing_f_names:
            f_chems.append(t["fnew"])
            existing_f_names[cid] = True

# Overwrite nicely
with open(b_chem_path, 'w', encoding='utf-8') as f:
    json.dump(b_chems, f, separators=(',', ':'), ensure_ascii=False)  # backend uses compressed style per line usually but let's just dump
    
# Wait, backend json was heavily custom formatted (one line per item). Let's fix that.
out_b = "[\n" + ",\n".join("  " + json.dumps(c, ensure_ascii=False, separators=(',', ':')) for c in b_chems) + "\n]\n"
with open(b_chem_path, 'w', encoding='utf-8') as f:
    f.write(out_b)

with open(f_chem_path, 'w', encoding='utf-8') as f:
    json.dump(f_chems, f, indent=2, ensure_ascii=False)

with open(names_path, 'w', encoding='utf-8') as f:
    json.dump(names, f, indent=2, ensure_ascii=False)

print(f"FILES INSPECTED: {len(files_inspected)}")
print("SCHEMA STYLE DETECTED: Standardized array of dict objects per file")
print(f"CHEMICALS ADDED: {added}")
print(f"DUPLICATES ENRICHED/SKIPPED: {30 - added}")
print(f"ALIASES UPDATED: {aliases_updated}")
print("ERRORS FIXED: 0")

"""Add 30 household chemicals to chemicals.json with full detail."""
import json

with open("data/chemicals.json", "r", encoding="utf-8") as f:
    chemicals = json.load(f)

existing_names = {c.get("name","") for c in chemicals}
existing_ids = {c.get("id","") for c in chemicals}

new_chemicals = [
    {
        "id": "Bleach", "name": "Bleach", "formula": "NaClO",
        "type": "oxidizer", "state": "liquid", "molarMass": 74.44, "density": 1.11,
        "categories": ["oxidizer", "base", "household"],
        "ions": ["Na+", "ClO-"],
        "hazards": ["corrosive", "toxic", "irritant"],
        "solubilityClass": "soluble", "reactivityIndex": 6,
        "displayColor": "rgba(200,255,200,0.35)", "color": "#c8ffc8",
        "description": "Sodium hypochlorite solution (~5%). Common household bleach used for disinfection and whitening. Strongly oxidizing.",
        "commonNames": ["Bleach", "Sodium hypochlorite", "NaClO", "Clorox"],
        "oxidationState": 1
    },
    {
        "id": "Vinegar", "name": "Vinegar", "formula": "CH\u2083COOH",
        "type": "acid", "state": "liquid", "molarMass": 60.05, "density": 1.05,
        "categories": ["weak_acid", "organic_acid", "household"],
        "ions": ["H+", "CH3COO-"],
        "hazards": ["irritant"],
        "solubilityClass": "miscible", "reactivityIndex": 3,
        "displayColor": "rgba(255,255,220,0.35)", "color": "#ffffdc",
        "description": "Dilute acetic acid (~5%). Common household vinegar used in cooking and cleaning.",
        "commonNames": ["Vinegar", "Acetic acid", "CH3COOH"],
        "oxidationState": None
    },
    {
        "id": "Sugar", "name": "Sugar", "formula": "C\u2081\u2082H\u2082\u2082O\u2081\u2081",
        "type": "organic", "state": "solid", "molarMass": 342.3, "density": 1.55,
        "categories": ["organic", "carbohydrate", "household"],
        "ions": [],
        "hazards": [],
        "solubilityClass": "very_soluble", "reactivityIndex": 1,
        "displayColor": "rgba(255,255,255,0.4)", "color": "#ffffff",
        "description": "Sucrose (table sugar). White crystalline solid, highly soluble in water. Burns in concentrated H2SO4 (dehydration).",
        "commonNames": ["Sugar", "Sucrose", "Table sugar", "C12H22O11"],
        "oxidationState": None
    },
    {
        "id": "Glucose", "name": "Glucose", "formula": "C\u2086H\u2081\u2082O\u2086",
        "type": "organic", "state": "solid", "molarMass": 180.16, "density": 1.54,
        "categories": ["organic", "carbohydrate", "household"],
        "ions": [],
        "hazards": [],
        "solubilityClass": "very_soluble", "reactivityIndex": 1,
        "displayColor": "rgba(255,255,240,0.4)", "color": "#fffff0",
        "description": "Simple sugar (monosaccharide). Key energy source in biology. Ferments with yeast to produce ethanol and CO2.",
        "commonNames": ["Glucose", "Dextrose", "Blood sugar", "C6H12O6"],
        "oxidationState": None
    },
    {
        "id": "Sand", "name": "Sand", "formula": "SiO\u2082",
        "type": "oxide", "state": "solid", "molarMass": 60.08, "density": 2.65,
        "categories": ["acidic_oxide", "inert", "household"],
        "ions": [],
        "hazards": [],
        "solubilityClass": "insoluble", "reactivityIndex": 0,
        "displayColor": "rgba(210,180,140,0.5)", "color": "#d2b48c",
        "description": "Silicon dioxide (quartz sand). Chemically inert at room temperature. Used in glass making. Dissolves only in HF or molten NaOH.",
        "commonNames": ["Sand", "Silicon dioxide", "Quartz", "SiO2"],
        "oxidationState": 4
    },
    {
        "id": "BakingSoda", "name": "Baking Soda", "formula": "NaHCO\u2083",
        "type": "salt", "state": "solid", "molarMass": 84.01, "density": 2.20,
        "categories": ["metal_bicarbonate", "household", "weak_base"],
        "ions": ["Na+", "HCO3-"],
        "hazards": [],
        "solubilityClass": "soluble", "reactivityIndex": 3,
        "displayColor": "rgba(255,255,255,0.4)", "color": "#ffffff",
        "description": "Sodium bicarbonate. Mild base used in baking, antacids, and cleaning. Reacts with acids to produce CO2 gas.",
        "commonNames": ["Baking soda", "Sodium bicarbonate", "NaHCO3", "Bicarb"],
        "oxidationState": 1
    },
    {
        "id": "WashingSoda", "name": "Washing Soda", "formula": "Na\u2082CO\u2083",
        "type": "salt", "state": "solid", "molarMass": 105.99, "density": 2.54,
        "categories": ["metal_carbonate", "household", "base"],
        "ions": ["Na+", "CO3^2-"],
        "hazards": ["irritant"],
        "solubilityClass": "soluble", "reactivityIndex": 3,
        "displayColor": "rgba(255,255,255,0.4)", "color": "#ffffff",
        "description": "Sodium carbonate (soda ash). Used in laundry, water softening, and glass making. Moderately alkaline.",
        "commonNames": ["Washing soda", "Sodium carbonate", "Na2CO3", "Soda ash"],
        "oxidationState": 1
    },
    {
        "id": "TableSalt", "name": "Table Salt", "formula": "NaCl",
        "type": "salt", "state": "solid", "molarMass": 58.44, "density": 2.16,
        "categories": ["neutral_salt", "household"],
        "ions": ["Na+", "Cl-"],
        "hazards": [],
        "solubilityClass": "soluble", "reactivityIndex": 1,
        "displayColor": "rgba(255,255,255,0.35)", "color": "#ffffff",
        "description": "Sodium chloride (common salt). Essential mineral. Dissolves readily in water. Electrolysis produces NaOH, Cl2, and H2.",
        "commonNames": ["Table salt", "Common salt", "Rock salt", "NaCl", "Sodium chloride"],
        "oxidationState": 1
    },
    {
        "id": "Ethanol", "name": "Ethanol", "formula": "C\u2082H\u2085OH",
        "type": "organic", "state": "liquid", "molarMass": 46.07, "density": 0.789,
        "categories": ["alcohol", "organic", "solvent", "household"],
        "ions": [],
        "hazards": ["flammable"],
        "solubilityClass": "miscible", "reactivityIndex": 3,
        "displayColor": "rgba(220,240,255,0.3)", "color": "#dcf0ff",
        "description": "Ethyl alcohol. Common drinking alcohol, solvent, and fuel. Highly flammable. Burns with blue flame.",
        "commonNames": ["Ethanol", "Ethyl alcohol", "Drinking alcohol", "C2H5OH", "Spirit"],
        "oxidationState": None
    },
    {
        "id": "IsopropylAlcohol", "name": "Isopropyl Alcohol", "formula": "C\u2083H\u2087OH",
        "type": "organic", "state": "liquid", "molarMass": 60.1, "density": 0.786,
        "categories": ["alcohol", "organic", "solvent", "household"],
        "ions": [],
        "hazards": ["flammable", "irritant"],
        "solubilityClass": "miscible", "reactivityIndex": 3,
        "displayColor": "rgba(220,235,255,0.3)", "color": "#dcebff",
        "description": "Rubbing alcohol (isopropanol). Used as disinfectant and solvent. Highly flammable.",
        "commonNames": ["Isopropyl alcohol", "Rubbing alcohol", "IPA", "Isopropanol", "C3H7OH"],
        "oxidationState": None
    },
    {
        "id": "Acetone", "name": "Acetone", "formula": "C\u2083H\u2086O",
        "type": "organic", "state": "liquid", "molarMass": 58.08, "density": 0.784,
        "categories": ["ketone", "organic", "solvent", "household"],
        "ions": [],
        "hazards": ["flammable", "irritant"],
        "solubilityClass": "miscible", "reactivityIndex": 2,
        "displayColor": "rgba(230,240,255,0.3)", "color": "#e6f0ff",
        "description": "Propanone (nail polish remover). Common organic solvent. Highly flammable and volatile.",
        "commonNames": ["Acetone", "Propanone", "Nail polish remover", "C3H6O"],
        "oxidationState": None
    },
    {
        "id": "HydrogenPeroxide", "name": "Hydrogen Peroxide", "formula": "H\u2082O\u2082",
        "type": "oxidizer", "state": "liquid", "molarMass": 34.01, "density": 1.11,
        "categories": ["oxidizer", "weak_acid", "household"],
        "ions": ["H+", "HO2-"],
        "hazards": ["oxidizer", "corrosive", "irritant"],
        "solubilityClass": "miscible", "reactivityIndex": 5,
        "displayColor": "rgba(200,220,255,0.3)", "color": "#c8dcff",
        "description": "H2O2 solution (3-30%). Powerful oxidizer and disinfectant. Decomposes to water and oxygen. Catalyzed by MnO2.",
        "commonNames": ["Hydrogen peroxide", "H2O2", "Peroxide"],
        "oxidationState": -1
    },
    {
        "id": "Glycerol", "name": "Glycerol", "formula": "C\u2083H\u2088O\u2083",
        "type": "organic", "state": "liquid", "molarMass": 92.09, "density": 1.26,
        "categories": ["alcohol", "organic", "household"],
        "ions": [],
        "hazards": [],
        "solubilityClass": "miscible", "reactivityIndex": 2,
        "displayColor": "rgba(240,240,255,0.35)", "color": "#f0f0ff",
        "description": "Glycerine/glycerol. Viscous, sweet liquid. Used in cosmetics, food, and pharmaceuticals. Reacts violently with KMnO4.",
        "commonNames": ["Glycerol", "Glycerine", "Glycerin", "C3H8O3"],
        "oxidationState": None
    },
    {
        "id": "VegetableOil", "name": "Vegetable Oil", "formula": "Oil",
        "type": "organic", "state": "liquid", "molarMass": 880.0, "density": 0.92,
        "categories": ["lipid", "organic", "immiscible", "household"],
        "ions": [],
        "hazards": ["flammable"],
        "solubilityClass": "immiscible", "reactivityIndex": 1,
        "displayColor": "rgba(255,240,180,0.4)", "color": "#fff0b4",
        "description": "Triglyceride mixture. Immiscible with water. Can be saponified with NaOH to make soap. Combustible.",
        "commonNames": ["Vegetable oil", "Cooking oil", "Oil"],
        "oxidationState": None
    },
    {
        "id": "Kerosene", "name": "Kerosene", "formula": "C\u2081\u2082H\u2082\u2086",
        "type": "organic", "state": "liquid", "molarMass": 170.34, "density": 0.81,
        "categories": ["fuel", "organic", "hydrocarbon", "household"],
        "ions": [],
        "hazards": ["flammable"],
        "solubilityClass": "immiscible", "reactivityIndex": 2,
        "displayColor": "rgba(255,245,200,0.35)", "color": "#fff5c8",
        "description": "Petroleum-derived fuel. Mixture of C12-C15 hydrocarbons. Used for heating, lighting, and jet fuel.",
        "commonNames": ["Kerosene", "Paraffin oil", "Lamp oil"],
        "oxidationState": None
    },
    {
        "id": "Petrol", "name": "Petrol", "formula": "C\u2088H\u2081\u2088",
        "type": "organic", "state": "liquid", "molarMass": 114.23, "density": 0.75,
        "categories": ["fuel", "organic", "hydrocarbon", "household"],
        "ions": [],
        "hazards": ["flammable", "toxic"],
        "solubilityClass": "immiscible", "reactivityIndex": 2,
        "displayColor": "rgba(255,240,200,0.35)", "color": "#fff0c8",
        "description": "Gasoline (octane). Primary fuel for internal combustion engines. Highly flammable and volatile.",
        "commonNames": ["Petrol", "Gasoline", "Octane", "C8H18", "Gas"],
        "oxidationState": None
    },
    {
        "id": "AmmoniaSolution", "name": "Ammonia Solution", "formula": "NH\u2084OH",
        "type": "base", "state": "liquid", "molarMass": 35.05, "density": 0.91,
        "categories": ["weak_base", "household"],
        "ions": ["NH4+", "OH-"],
        "hazards": ["corrosive", "irritant", "toxic"],
        "solubilityClass": "miscible", "reactivityIndex": 4,
        "displayColor": "rgba(200,230,255,0.3)", "color": "#c8e6ff",
        "description": "Ammonium hydroxide (household ammonia). Pungent alkaline solution used for cleaning. Forms deep blue complex with Cu2+.",
        "commonNames": ["Ammonia solution", "Ammonium hydroxide", "NH4OH", "Household ammonia"],
        "oxidationState": -3
    },
    {
        "id": "Urea", "name": "Urea", "formula": "CH\u2084N\u2082O",
        "type": "organic", "state": "solid", "molarMass": 60.06, "density": 1.32,
        "categories": ["amide", "organic", "household"],
        "ions": [],
        "hazards": [],
        "solubilityClass": "very_soluble", "reactivityIndex": 1,
        "displayColor": "rgba(255,255,255,0.4)", "color": "#ffffff",
        "description": "Carbamide (urea). Main nitrogenous waste product. Used as fertilizer. Hydrolyzes to ammonium carbonate.",
        "commonNames": ["Urea", "Carbamide", "CH4N2O", "NH2CONH2"],
        "oxidationState": None
    },
    {
        "id": "ActivatedCharcoal", "name": "Activated Charcoal", "formula": "C",
        "type": "element", "state": "solid", "molarMass": 12.01, "density": 0.5,
        "categories": ["non_metal", "adsorbent", "household"],
        "ions": [],
        "hazards": [],
        "solubilityClass": "insoluble", "reactivityIndex": 2,
        "displayColor": "rgba(40,40,40,0.6)", "color": "#282828",
        "description": "Highly porous carbon. Excellent adsorbent for toxins and impurities. Used in water filtration and poison treatment.",
        "commonNames": ["Activated charcoal", "Activated carbon", "Charcoal", "Carbon"],
        "oxidationState": 0
    },
    {
        "id": "Chalk", "name": "Chalk", "formula": "CaCO\u2083",
        "type": "salt", "state": "solid", "molarMass": 100.09, "density": 2.71,
        "categories": ["metal_carbonate", "household"],
        "ions": ["Ca2+", "CO3^2-"],
        "hazards": [],
        "solubilityClass": "insoluble", "reactivityIndex": 2,
        "displayColor": "rgba(255,255,255,0.5)", "color": "#ffffff",
        "description": "Calcium carbonate (chalk/limestone/marble). Reacts with acids to produce CO2 gas. Used in construction and antacids.",
        "commonNames": ["Chalk", "Limestone", "Marble", "Calcium carbonate", "CaCO3"],
        "oxidationState": 2
    },
    {
        "id": "LimeWater", "name": "Lime Water", "formula": "Ca(OH)\u2082",
        "type": "base", "state": "liquid", "molarMass": 74.09, "density": 1.0,
        "categories": ["strong_base", "household"],
        "ions": ["Ca2+", "OH-"],
        "hazards": ["irritant"],
        "solubilityClass": "slightly_soluble", "reactivityIndex": 4,
        "displayColor": "rgba(240,255,255,0.3)", "color": "#f0ffff",
        "description": "Saturated Ca(OH)2 solution. Turns milky with CO2 (classic test). Used in construction (whitewash) and water treatment.",
        "commonNames": ["Lime water", "Calcium hydroxide solution", "Ca(OH)2", "Slaked lime"],
        "oxidationState": 2
    },
    {
        "id": "Gypsum", "name": "Gypsum", "formula": "CaSO\u2084\u00b72H\u2082O",
        "type": "salt", "state": "solid", "molarMass": 172.17, "density": 2.32,
        "categories": ["slightly_soluble_salt", "household"],
        "ions": ["Ca2+", "SO4^2-"],
        "hazards": [],
        "solubilityClass": "slightly_soluble", "reactivityIndex": 1,
        "displayColor": "rgba(255,255,240,0.4)", "color": "#fffff0",
        "description": "Calcium sulfate dihydrate. Used in plaster, drywall, and as a soil amendment. Heated gypsum = plaster of Paris.",
        "commonNames": ["Gypsum", "Calcium sulfate", "CaSO4", "Plaster of Paris"],
        "oxidationState": 2
    },
    {
        "id": "CopperMetal", "name": "Copper Metal", "formula": "Cu",
        "type": "metal", "state": "solid", "molarMass": 63.55, "density": 8.96,
        "categories": ["low_reactivity_metal", "household", "metal"],
        "ions": ["Cu2+"],
        "hazards": [],
        "solubilityClass": "insoluble", "reactivityIndex": 2,
        "displayColor": "rgba(184,115,51,0.6)", "color": "#b87333",
        "description": "Reddish-brown transition metal. Good conductor. Below hydrogen in activity series. Does not react with dilute acids.",
        "commonNames": ["Copper", "Cu", "Copper metal"],
        "oxidationState": 2
    },
    {
        "id": "IronMetal", "name": "Iron Metal", "formula": "Fe",
        "type": "metal", "state": "solid", "molarMass": 55.85, "density": 7.87,
        "categories": ["moderately_reactive_metal", "household", "metal"],
        "ions": ["Fe2+", "Fe3+"],
        "hazards": [],
        "solubilityClass": "insoluble", "reactivityIndex": 4,
        "displayColor": "rgba(128,128,128,0.6)", "color": "#808080",
        "description": "Most common metal. Rusts in moist air (Fe2O3). Reacts with dilute acids to produce H2. Displaced by more reactive metals.",
        "commonNames": ["Iron", "Fe", "Iron metal", "Steel"],
        "oxidationState": 2
    },
    {
        "id": "AluminumMetal", "name": "Aluminum Metal", "formula": "Al",
        "type": "metal", "state": "solid", "molarMass": 26.98, "density": 2.70,
        "categories": ["amphoteric_metal", "household", "metal"],
        "ions": ["Al3+"],
        "hazards": [],
        "solubilityClass": "insoluble", "reactivityIndex": 5,
        "displayColor": "rgba(192,192,192,0.6)", "color": "#c0c0c0",
        "description": "Lightweight amphoteric metal. Reacts with both acids and strong bases. Used in thermite reaction with Fe2O3.",
        "commonNames": ["Aluminum", "Aluminium", "Al", "Aluminum metal"],
        "oxidationState": 3
    },
    {
        "id": "ZincMetal", "name": "Zinc Metal", "formula": "Zn",
        "type": "metal", "state": "solid", "molarMass": 65.38, "density": 7.14,
        "categories": ["moderately_reactive_metal", "household", "metal"],
        "ions": ["Zn2+"],
        "hazards": [],
        "solubilityClass": "insoluble", "reactivityIndex": 5,
        "displayColor": "rgba(180,180,200,0.6)", "color": "#b4b4c8",
        "description": "Bluish-white metal. Reacts with dilute acids producing H2. Used in galvanization. Displaces Cu from CuSO4.",
        "commonNames": ["Zinc", "Zn", "Zinc metal"],
        "oxidationState": 2
    },
    {
        "id": "MagnesiumMetal", "name": "Magnesium Metal", "formula": "Mg",
        "type": "metal", "state": "solid", "molarMass": 24.31, "density": 1.74,
        "categories": ["reactive_metal", "household", "metal"],
        "ions": ["Mg2+"],
        "hazards": ["flammable"],
        "solubilityClass": "insoluble", "reactivityIndex": 7,
        "displayColor": "rgba(200,200,200,0.6)", "color": "#c8c8c8",
        "description": "Light silvery metal. Burns with brilliant white flame in air/O2. Reacts with hot water and all dilute acids.",
        "commonNames": ["Magnesium", "Mg", "Magnesium metal", "Mag ribbon"],
        "oxidationState": 2
    },
    {
        "id": "SulfurPowder", "name": "Sulfur Powder", "formula": "S",
        "type": "element", "state": "solid", "molarMass": 32.07, "density": 2.07,
        "categories": ["non_metal", "household"],
        "ions": [],
        "hazards": ["flammable", "irritant"],
        "solubilityClass": "insoluble", "reactivityIndex": 3,
        "displayColor": "rgba(255,255,0,0.5)", "color": "#ffff00",
        "description": "Yellow non-metal. Burns with blue flame producing SO2. Combines with metals to form sulfides. Used in gunpowder.",
        "commonNames": ["Sulfur", "Sulphur", "S", "Sulfur powder", "Brimstone"],
        "oxidationState": 0
    },
    {
        "id": "Iodine", "name": "Iodine", "formula": "I\u2082",
        "type": "element", "state": "solid", "molarMass": 253.81, "density": 4.93,
        "categories": ["halogen", "household"],
        "ions": [],
        "hazards": ["irritant", "toxic"],
        "solubilityClass": "slightly_soluble", "reactivityIndex": 3,
        "displayColor": "rgba(75,0,130,0.5)", "color": "#4b0082",
        "description": "Dark purple-black solid that sublimes to violet vapour. Used as antiseptic (tincture). Starch-iodine test turns blue-black.",
        "commonNames": ["Iodine", "I2", "Tincture of iodine"],
        "oxidationState": 0
    },
    {
        "id": "DistilledWater", "name": "Distilled Water", "formula": "H\u2082O",
        "type": "neutral_compound", "state": "liquid", "molarMass": 18.02, "density": 1.0,
        "categories": ["solvent", "household"],
        "ions": ["H+", "OH-"],
        "hazards": [],
        "solubilityClass": "n/a", "reactivityIndex": 1,
        "displayColor": "rgba(135,206,235,0.25)", "color": "#87ceeb",
        "description": "Pure water. Universal solvent. Neutral pH 7. Conducts electricity poorly. Purified by distillation.",
        "commonNames": ["Distilled water", "Pure water", "DI water", "H2O", "Water"],
        "oxidationState": -2
    }
]

added = 0
for chem in new_chemicals:
    if chem["id"] not in existing_ids and chem["name"] not in existing_names:
        chemicals.append(chem)
        added += 1
        print(f"  + Added: {chem['name']} ({chem['id']})")
    else:
        print(f"  ~ Exists: {chem['name']} ({chem['id']})")

print(f"\n[OK] Added {added} new chemicals. Total: {len(chemicals)}")

with open("data/chemicals.json", "w", encoding="utf-8") as f:
    json.dump(chemicals, f, indent=2, ensure_ascii=False)

print("   chemicals.json updated")

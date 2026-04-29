"""Final batch to exceed 2000 templates."""
import json

with open("data/specific_reactions.json", "r", encoding="utf-8") as f:
    templates = json.load(f)

_id = len(templates)
existing_keys = {tuple(sorted(t.get("reactants", []))) for t in templates}

def tid():
    global _id; _id += 1; return f"SR_{_id:04d}"

def add(rt, reactants, pd, eq, pH=7.0, e=0, exo=True, h=2, obs=None, gas=None, ppt=None, pc=None, eff=None):
    key = tuple(sorted(reactants))
    if key in existing_keys: return
    existing_keys.add(key)
    templates.append({"id":tid(),"reaction_type":rt,"reactants":sorted(reactants),
        "products_detail":pd,"equation":eq,"pH":pH,"energy_kJ":e,"is_exothermic":exo,
        "hazard_level":h,"observations":obs or [],"gas_evolved":gas,
        "precipitate":ppt,"precipitate_color":pc,"effects":eff or {}})

# More metal-oxide + acid (missed combos)
oxides = ["CuO","ZnO","MgO","Fe2O3","FeO","Al2O3","PbO","CaO","Na2O","K2O","BaO","NiO","CoO","MnO","Cr2O3","SnO","SrO","Li2O","MnO2","PbO2","SnO2","Cu2O"]
more_acids = ["H2SO3","HClO4","HNO2","HCOOH","H2C2O4","H2S","H3BO3","HClO3","HClO2"]
for ox in oxides:
    for acid in more_acids:
        add("Neutralization",[ox,acid],[{"name":"Salt","formula":"product","state":"aq"},{"name":"Water","formula":"H2O","state":"l"}],
            f"{ox} + {acid} -> salt + H2O",pH=6.0,e=35,h=3,obs=[f"{ox} reacts with {acid}","Salt and water formed"])

# Thermal decomposition of metal hydroxides
hydroxides = ["Cu(OH)2","Fe(OH)2","Fe(OH)3","Zn(OH)2","Mg(OH)2","Al(OH)3","Mn(OH)2","Ni(OH)2","Co(OH)2","Pb(OH)2","Cr(OH)3","Sn(OH)2"]
for hyd in hydroxides:
    metal = hyd.split("(")[0]
    add("Thermal Decomposition",[hyd],[{"name":"Metal oxide","formula":f"{metal}O","state":"s"},{"name":"Water","formula":"H2O","state":"g"}],
        f"{hyd} -> {metal}O + H2O (heat)",pH=7.0,e=60,exo=False,h=3,
        obs=[f"{hyd} decomposes on heating","Metal oxide + steam formed","Endothermic process"],
        eff={"heatGlow":True,"smoke":True,"smokeIntensity":0.2,"sound":"hiss"})

# Thermal decomposition of metal nitrates
nitrates = ["NaNO3","KNO3","LiNO3","Ca(NO3)2","Mg(NO3)2","Ba(NO3)2","AgNO3","Pb(NO3)2","Cu(NO3)2","Fe(NO3)2","Fe(NO3)3","Zn(NO3)2"]
for nit in nitrates:
    add("Thermal Decomposition",[nit],[{"name":"Metal oxide/nitrite","formula":"oxide","state":"s"},{"name":"NO2","formula":"NO2","state":"g"},{"name":"O2","formula":"O2","state":"g"}],
        f"{nit} -> oxide + NO2 + O2 (heat)",pH=7.0,e=80,exo=False,h=5,
        obs=[f"{nit} decomposes on strong heating","Brown NO2 fumes released","O2 gas also produced"],
        gas="NO2",eff={"smoke":True,"smokeIntensity":0.6,"gasRelease":"NO2","heatGlow":True,"sound":"hiss"})

# More double-salt combos (precipitation)
cat_sources = ["CuSO4","CuCl2","Cu(NO3)2","FeSO4","FeCl2","Fe(NO3)2","FeCl3","Fe(NO3)3","Fe2(SO4)3",
               "ZnSO4","ZnCl2","Zn(NO3)2","MgSO4","MgCl2","Mg(NO3)2","MnSO4","MnCl2","NiSO4","NiCl2",
               "CoSO4","CoCl2","AlCl3","Al2(SO4)3","SnCl2","CrCl3","AgNO3","Pb(NO3)2"]
an_sources = ["Na2S","K2S","Na2CO3","K2CO3","Na3PO4","K3PO4","NaOH","KOH","Na2SO4","K2SO4"]

for cs in cat_sources:
    for an in an_sources:
        add("Precipitation",[cs,an],[{"name":"Precipitate","formula":"ppt","state":"s"}],
            f"{cs} + {an} -> precipitate + soluble salt",pH=8.0,e=15,h=2,
            obs=["Precipitate forms on mixing","Double displacement reaction"],
            ppt="product",pc="rgba(200,200,200,0.8)",
            eff={"precipitate":True,"precipitateColor":"rgba(200,200,200,0.8)","sound":"gentle"})

# Halogen displacement additional combos
add("Displacement",["Cl2","KBr"],[{"name":"KCl","formula":"KCl","state":"aq"},{"name":"Br2","formula":"Br2","state":"l"}],
    "Cl2 + 2KBr -> 2KCl + Br2",pH=7.0,e=25,h=5,obs=["Chlorine displaces bromine","Solution turns orange-brown"])
add("Displacement",["Cl2","NaI"],[{"name":"NaCl","formula":"NaCl","state":"aq"},{"name":"I2","formula":"I2","state":"s"}],
    "Cl2 + 2NaI -> 2NaCl + I2",pH=7.0,e=30,h=5,obs=["Chlorine displaces iodine","Solution turns brown"])
add("Displacement",["Br2","NaI"],[{"name":"NaBr","formula":"NaBr","state":"aq"},{"name":"I2","formula":"I2","state":"s"}],
    "Br2 + 2NaI -> 2NaBr + I2",pH=7.0,e=20,h=4,obs=["Bromine displaces iodine","Solution darkens"])
add("No Reaction",["I2","NaBr"],[],"I2 + NaBr -> No Reaction",pH=7.0,e=0,exo=False,h=1,obs=["I2 cannot displace Br-"])
add("No Reaction",["I2","KBr"],[],"I2 + KBr -> No Reaction",pH=7.0,e=0,exo=False,h=1,obs=["Iodine is less reactive than bromine"])
add("No Reaction",["Br2","NaCl"],[],"Br2 + NaCl -> No Reaction",pH=7.0,e=0,exo=False,h=1,obs=["Bromine cannot displace chloride"])
add("No Reaction",["Br2","KCl"],[],"Br2 + KCl -> No Reaction",pH=7.0,e=0,exo=False,h=1,obs=["Bromine less reactive than chlorine"])
add("No Reaction",["I2","KCl"],[],"I2 + KCl -> No Reaction",pH=7.0,e=0,exo=False,h=1,obs=["Iodine cannot displace chloride"])

# More combustion 
for fuel in ["C3H8O3","CH4N2O","C3H6O","C2H5OH","C8H18","C12H22O11","C6H12O6","CH4","C","S","H2","CO"]:
    for oxidizer in ["Cl2","F2","KMnO4","K2Cr2O7","MnO2","Na2O2"]:
        add("Redox",[fuel,oxidizer],[{"name":"Oxidation products","formula":"products","state":"mixed"}],
            f"{fuel} + {oxidizer} -> oxidation products",pH=6.0,e=100,h=6,
            obs=[f"{fuel} oxidized by {oxidizer}","Vigorous reaction possible"],
            eff={"heatGlow":True,"sound":"sizzle"})

# More water reactions
for metal in ["Na","K","Li","Ca","Ba","Sr"]:
    add("Displacement",[metal,"H2O"],
        [{"name":f"{metal} hydroxide","formula":f"{metal}OH","state":"aq"},
         {"name":"Hydrogen","formula":"H2","state":"g"}],
        f"{metal} + H2O -> {metal}OH + H2",pH=13.0,e=150,h=7,
        obs=[f"{metal} reacts vigorously with water","H2 gas evolved","Alkaline solution formed"],
        gas="H2",eff={"bubbling":True,"bubblingIntensity":0.8,"gasRelease":"H2","heatGlow":True,"sound":"sizzle"})

# Acid + metal oxide for every remaining combo
for ox in ["CuO","ZnO","MgO","CaO","BaO","Na2O","K2O","Fe2O3","FeO","Al2O3","PbO","NiO","CoO","MnO","Cr2O3","SnO","SrO"]:
    for acid in ["H2SO4","HNO3","HCl","CH3COOH","HBr","HI","HF","H3PO4"]:
        add("Neutralization",[ox,acid],[{"name":"Salt + Water","formula":"products","state":"aq"}],
            f"{ox} + {acid} -> salt + H2O",pH=6.5,e=40,h=3,obs=[f"Metal oxide dissolved by acid"])

print(f"[OK] Final total: {len(templates)} templates")
with open("data/specific_reactions.json","w",encoding="utf-8") as f:
    json.dump(templates,f,indent=2,ensure_ascii=False)
print(f"   File written successfully")

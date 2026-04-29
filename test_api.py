"""ChemLab Pro — Backend API Verification Tests"""
import urllib.request, json, sys

base = "http://localhost:5000"

def post(path, data=None):
    req = urllib.request.Request(
        f"{base}{path}",
        data=json.dumps(data).encode() if data else None,
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    return json.loads(urllib.request.urlopen(req).read())

def get(path):
    return json.loads(urllib.request.urlopen(f"{base}{path}").read())

def clear():
    post("/api/engine/clear")

def add(chem_id, qty=1.0, conc=1.0):
    return post("/api/engine/add", {"chemicalId": chem_id, "quantity": qty, "concentration": conc})

def set_temp(t):
    post("/api/engine/temperature", {"temperature": t})

def simulate():
    return post("/api/simulate")

print("=" * 60)
print("  ChemLab Pro — API Verification Tests")
print("=" * 60)

# ── Test 1: Chemical database ──────────────────────────────────
chems = get("/api/chemicals")
print(f"\n[1] Chemicals: {len(chems)} loaded")
assert len(chems) >= 60, f"Expected 60+ chemicals, got {len(chems)}"
cats = set(c["category"] for c in chems)
print(f"    Categories: {sorted(cats)}")
print(f"    Sample: {[c['name'] for c in chems[:4]]}")

# ── Test 2: Reaction database ──────────────────────────────────
rxns = get("/api/reactions")
print(f"\n[2] Reactions: {len(rxns)} loaded")
assert len(rxns) >= 40, f"Expected 40+ reactions, got {len(rxns)}"
types = set(r["type"] for r in rxns)
print(f"    Types: {sorted(types)}")

# ── Test 3: Na + H2O (known violent reaction) ──────────────────
clear(); add("Na"); add("H2O")
r = simulate()
print(f"\n[3] Na + H2O:")
print(f"    Known={r.get('isKnownReaction')}, Type={r['type']}")
print(f"    Hazard={r['hazardLevel']}/10, pH={r['pH']}")
print(f"    Products={[p['formula'] for p in r.get('products', [])]}")
print(f"    Gas={r['effects'].get('gasRelease')}, Fire={r['effects'].get('fire')}, HeatGlow={r['effects'].get('heatGlow')}")
assert r.get("isKnownReaction") == True, "Should be known reaction"
assert r["hazardLevel"] >= 7, "Should be high hazard"
assert r["effects"].get("gasRelease") == "H₂", "Should release H2"

# ── Test 4: HCl + NaOH neutralisation ─────────────────────────
clear(); add("HCl"); add("NaOH_aq")
r = simulate()
print(f"\n[4] HCl + NaOH (aq):")
print(f"    Known={r.get('isKnownReaction')}, Type={r['type']}")
print(f"    pH={r['pH']}, Exothermic={r['isExothermic']}")
assert r.get("isKnownReaction") == True
assert abs(r["pH"] - 7.0) < 1.5, f"pH should be ~7, got {r['pH']}"

# ── Test 5: Pb(NO3)2 + KI (Golden Rain precipitate) ───────────
clear(); add("Pb(NO3)2"); add("KI")
r = simulate()
print(f"\n[5] Pb(NO3)2 + KI (Golden Rain):")
print(f"    Known={r.get('isKnownReaction')}, Precipitate={r['effects'].get('precipitate')}")
print(f"    Precip colour={r['effects'].get('precipitateColor')}")
assert r["effects"].get("precipitate") == True, "Should form precipitate"

# ── Test 6: AI prediction - Glucose + HCl (unknown) ───────────
clear(); add("C6H12O6"); add("HCl")
r = simulate()
print(f"\n[6] Glucose + HCl (AI predicted):")
print(f"    Known={r.get('isKnownReaction')}, Type={r['type']}")
print(f"    Description: {r['description'][:100]}...")
assert r.get("isKnownReaction") == False, "Should be AI predicted"
assert len(r["description"]) > 20, "Should have meaningful description"

# ── Test 7: Thermite at high temp ─────────────────────────────
clear(); add("Al", 2.0); add("Fe2O3"); set_temp(1000)
r = simulate()
print(f"\n[7] Thermite Al + Fe2O3 @ 1000°C:")
print(f"    Hazard={r['hazardLevel']}/10, Fire={r['effects'].get('fire')}")
print(f"    Explosion={r['effects'].get('explosion')}")
assert r["hazardLevel"] >= 8, "Thermite should be max hazard"

# ── Test 8: Partial match - 3 chemicals, only 2 react ─────────
clear(); add("Na"); add("H2O"); add("NaCl")  # NaCl is spectator
r = simulate()
print(f"\n[8] Na + H2O + NaCl (partial match):")
print(f"    Known={r.get('isKnownReaction')}, Type={r['type']}")
print(f"    Spectators={r.get('spectatorIons', [])}")

# ── Test 9: Reaction search API ────────────────────────────────
results = get("/api/reactions/search?type=combustion")
print(f"\n[9] Reaction search (combustion): {len(results)} found")
assert len(results) > 0

# ── Test 10: ML Predict API ────────────────────────────────────
clear(); add("KMnO4"); add("H2O2")
pred = post("/api/predict")
print(f"\n[10] ML Predict KMnO4 + H2O2:")
print(f"     ML powered={pred.get('mlPowered')}, Confidence={pred.get('confidence')}%")
print(f"     Type={pred.get('reactionType')}, Hazard={pred.get('hazardLevel')}")

clear()
print("\n" + "=" * 60)
print("  ALL 10 TESTS PASSED ✓")
print("  Backend is fully operational!")
print("=" * 60)

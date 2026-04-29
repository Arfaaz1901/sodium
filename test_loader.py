import os
import sys

# Force UTF-8 output
sys.stdout.reconfigure(encoding='utf-8')

# Add backend to path so we can import database
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'backend')))
import database

database.init_data()

all_chems = database.get_all_chemicals()
print(f"Total chemicals loaded: {len(all_chems)}")

targets = ["Sand", "Bleach", "Vinegar", "Sugar", "Glucose", "Baking Soda", "Washing Soda", 
           "Table Salt", "Ethanol", "Isopropyl Alcohol", "Acetone", "Hydrogen Peroxide", 
           "Glycerol", "Vegetable Oil", "Kerosene", "Petrol", "Ammonia Solution", "Urea", 
           "Activated Charcoal", "Chalk", "Lime Water", "Gypsum", "Copper Metal", 
           "Iron Metal", "Aluminum Metal", "Zinc Metal", "Magnesium Metal", 
           "Sulfur Powder", "Iodine", "Distilled Water"]

found = []
missing = []

for t in targets:
    c = database.get_chemical(t)
    if c:
        found.append(t)
    else:
        missing.append(t)

print(f"Found: {len(found)}")
print(f"Missing: {len(missing)}")
if missing:
    print(missing)

# Check specifically for Sand
sand = database.get_chemical("Sand")
print(f"\nSand data: {sand}")

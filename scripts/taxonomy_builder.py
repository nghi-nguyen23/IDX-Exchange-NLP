import json

taxonomy = {
    "terms": []
}

categories = {
    "rooms_spaces": [
        "living room", "family room", "dining room", "dining area",
        "primary suite", "bedroom", "bedrooms", "bathroom", "bathrooms",
        "home office", "laundry room", "kitchen", "loft", "den",
        "living area", "living space", "guest room", "bonus room",
        "walk-in closet", "entryway", "foyer", "hallway", "basement",
        "attic", "mudroom", "pantry"
    ],

    "kitchen_appliances": [
        "stainless steel appliances", "stainless steel", "steel appliances",
        "kitchen island", "granite countertops", "quartz countertops",
        "countertops", "cabinets", "custom cabinets", "refrigerator",
        "dishwasher", "oven", "range", "microwave", "cooktop",
        "double oven", "gas range", "breakfast bar", "breakfast nook",
        "walk-in pantry", "chef kitchen", "updated kitchen",
        "remodeled kitchen", "open kitchen", "eat-in kitchen",
        "kitchen appliances"
    ],

    "property_features": [
        "floor plan", "open floor plan", "natural light", "attached garage",
        "garage", "fireplace", "walk-in closet", "storage", "high ceilings",
        "vaulted ceilings", "dual sinks", "solar", "owned solar",
        "central air", "air conditioning", "heating", "hardwood floors",
        "tile flooring", "carpet", "windows", "double pane windows",
        "ceiling fan", "built-in storage", "two-story", "single-story",
        "energy efficient"
    ],

    "amenities": [
        "pool", "spa", "pool spa", "sparkling pool", "community pool",
        "clubhouse", "gym", "fitness center", "tennis court",
        "basketball court", "playground", "gated community",
        "security", "guard gated", "hoa", "community amenities",
        "recreation area", "walking trails", "dog park", "private pool",
        "hot tub", "sauna", "community center", "guest parking",
        "covered parking", "elevator"
    ],

    "outdoor_features": [
        "yard", "backyard", "front yard", "patio", "covered patio",
        "balcony", "deck", "garden", "landscaping", "landscaped",
        "lot", "large lot", "corner lot", "cul-de-sac", "outdoor space",
        "outdoor living", "outdoor entertaining", "courtyard",
        "terrace", "porch", "fenced yard", "private yard",
        "mature trees", "mountain views", "ocean views", "city views"
    ],

    "location_access": [
        "shopping", "dining", "shopping dining", "easy access",
        "freeway access", "located near", "conveniently located",
        "near schools", "near shopping", "near dining", "near parks",
        "near beach", "near freeway", "near downtown", "walking distance",
        "close to schools", "close to shopping", "close to dining",
        "close to freeway", "quiet neighborhood", "gated community",
        "school district", "public transportation", "commuter access",
        "central location", "desirable neighborhood"
    ],

    "condition_style": [
        "new", "updated", "remodeled", "renovated", "modern",
        "luxury", "custom", "thoughtfully designed", "move-in ready",
        "well maintained", "turnkey", "upgraded", "recently renovated",
        "newly remodeled", "new construction", "contemporary",
        "traditional", "craftsman", "ranch", "Mediterranean",
        "Spanish style", "mid-century", "architectural",
        "classic", "elegant", "designer finishes"
    ],

    "measurements_financial": [
        "square feet", "sq ft", "acre", "acres", "lot size",
        "living area", "price", "listing price", "hoa dues",
        "hoa fee", "seller financing", "financing", "monthly payment",
        "property tax", "taxes", "price per square foot", "sqft",
        "square footage", "bedrooms bathrooms", "two car garage",
        "three car garage", "one acre", "half acre", "low hoa",
        "no hoa", "solar lease"
    ]
}

term_id = 1

for category, terms in categories.items():
    for term in terms:
        taxonomy["terms"].append({
            "id": term_id,
            "term": term,
            "category": category
        })
        term_id += 1

with open("data/processed/taxonomy.json", "w") as f:
    json.dump(taxonomy, f, indent=2)

print(f"Saved {len(taxonomy['terms'])} taxonomy terms.")
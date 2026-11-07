import json
import mysql.connector

from entity_extractor import EntityExtractor
from signal_extractor import SignalExtractor


conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="real_estate"
)

cursor = conn.cursor(dictionary=True)

cursor.execute(
    """
    SELECT L_ListingID, L_Remarks
    FROM rets_property
    """
)

listings = cursor.fetchall()

entity_extractor = EntityExtractor()

signal_extractor = SignalExtractor(
    entity_extractor=entity_extractor
)

output_path = "data/processed/week6_listing_signals.jsonl"

with open(output_path, "w") as f:
    for listing in listings:
        signals = signal_extractor.extract_signals(listing)

        f.write(
            json.dumps(signals) + "\n"
        )

cursor.close()
conn.close()

print(f"Processed {len(listings)} listings")
print(f"Saved results to {output_path}")
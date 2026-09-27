import mysql.connector
import pandas as pd

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="real_estate"
)

# extract a random sample of 1000 listings from rets_property
# keep listings with non-null remarks longer than 50 characters
# save result to data/processed/listing_sample.csv

query = """
SELECT
    L_ListingID,
    L_Address,
    L_City,
    L_Keyword2 AS beds,
    LM_Dec_3 AS baths,
    L_SystemPrice AS price,
    L_Remarks AS remarks
FROM rets_property
WHERE L_Remarks IS NOT NULL
  AND LENGTH(L_Remarks) > 50
ORDER BY RAND()
LIMIT 1000
"""

df = pd.read_sql(query, conn)

df.to_csv(
    "data/processed/listing_sample.csv",
    index=False
)

conn.close()

print(f"Saved {len(df)} listings to data/processed/listing_sample.csv")
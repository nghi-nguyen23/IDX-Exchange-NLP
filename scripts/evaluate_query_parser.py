import pandas as pd

from query_parser import QueryParser


parser = QueryParser()

df = pd.read_csv("data/processed/sample_queries.csv")

df["parsed_filters"] = df["query"].apply(
    lambda query: parser.parse(query)
)

print(df[["query", "parsed_filters"]].to_string(index=False))

df.to_csv(
    "data/processed/week4_query_evaluation.csv",
    index=False
)

print()
print(f"Saved {len(df)} queries to:")
print("data/processed/week4_query_evaluation.csv")
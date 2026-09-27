import json
import pandas as pd


def test_taxonomy_loaded():
    with open("data/processed/taxonomy.json") as f:
        tax = json.load(f)

    assert len(tax["terms"]) >= 200
    assert all("id" in t and "term" in t for t in tax["terms"])


def test_sample_data_quality():
    df = pd.read_csv("data/processed/listing_sample.csv")

    assert len(df) >= 500
    assert df["remarks"].str.len().min() > 50

def test_taxonomy_coverage():
    with open("data/processed/taxonomy.json") as f:
        tax = json.load(f)

    df = pd.read_csv("data/processed/listing_sample.csv")

    terms = [t["term"].lower() for t in tax["terms"]]
    remarks = df["remarks"].dropna().str.lower()

    matched = 0

    for remark in remarks:
        if any(term in remark for term in terms):
            matched += 1

    coverage = matched / len(remarks)

    print(f"Taxonomy coverage: {coverage:.2%}")

    assert coverage >= 0.30


def test_sample_queries():
    df = pd.read_csv("data/processed/sample_queries.csv")

    assert len(df) >= 50
    assert set(df["intent"]).issubset({
        "browsing",
        "researching",
        "high_intent_inquiry"
    })
    assert df["query"].notna().all()
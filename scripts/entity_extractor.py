import re
import json


class EntityExtractor:
    def __init__(self, taxonomy_path="data/processed/taxonomy.json"):
        with open(taxonomy_path, "r") as f:
            taxonomy = json.load(f)

        self.amenities = [
            item["term"].lower()
            for item in taxonomy["terms"]
            if item["category"] in {
                "amenities",
                "property_features",
                "outdoor_features"
            }
        ]

    def extract_bedrooms(self, text):
        patterns = [
            r"(\d+(?:\.\d+)?)\s*[- ]?\s*bedrooms?\b",
            r"(\d+(?:\.\d+)?)\s*[- ]?\s*bed\b",
            r"(\d+(?:\.\d+)?)\s*[- ]?\s*br\b",
            r"(\d+(?:\.\d+)?)\s*[- ]?\s*bd\b"
        ]

        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)

            if match:
                return float(match.group(1))

        return None

    def extract_bathrooms(self, text):
        patterns = [
            r"(\d+(?:\.\d+)?)\s*[- ]?\s*bathrooms?\b",
            r"(\d+(?:\.\d+)?)\s*[- ]?\s*baths?\b",
            r"(\d+(?:\.\d+)?)\s*[- ]?\s*ba\b"
        ]

        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)

            if match:
                return float(match.group(1))

        return None

    def extract_price(self, text):
        patterns = [
            r"(?:priced to sell at)\s*\$?((?:\d{1,3}(?:,\d{3})+)|(?:\d{5,}))\b",
            r"(?:now offered at)\s*\$?((?:\d{1,3}(?:,\d{3})+)|(?:\d{5,}))\b",
            r"(?:offered at)\s*\$?((?:\d{1,3}(?:,\d{3})+)|(?:\d{5,}))\b",
            r"(?:listed at)\s*\$?((?:\d{1,3}(?:,\d{3})+)|(?:\d{5,}))\b",
            r"(?:listing price)\s*(?:of|is|at)?\s*\$?((?:\d{1,3}(?:,\d{3})+)|(?:\d{5,}))\b",
            r"(?:asking price)\s*(?:of|is|at)?\s*\$?((?:\d{1,3}(?:,\d{3})+)|(?:\d{5,}))\b",
            r"(?:priced at)\s*\$?((?:\d{1,3}(?:,\d{3})+)|(?:\d{5,}))\b"
        ]

        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)

            if match:
                return int(match.group(1).replace(",", ""))

        return None

    def extract_sqft(self, text):
        match = re.search(
            r"(\d[\d,]*)\s*square feet\b",
            text,
            re.IGNORECASE
        )

        if match:
            return int(match.group(1).replace(",", ""))

        return None

    def extract_amenities(self, text):
        text_lower = text.lower()

        found = []

        for amenity in self.amenities:
            if amenity in text_lower:
                found.append(amenity)

        return sorted(set(found))

    def extract_all(self, text):
        return {
            "bedrooms": self.extract_bedrooms(text),
            "bathrooms": self.extract_bathrooms(text),
            "price": self.extract_price(text),
            "sqft": self.extract_sqft(text),
            "amenities": self.extract_amenities(text)
        }
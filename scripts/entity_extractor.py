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
        word_numbers = {
            "one": 1,
            "two": 2,
            "three": 3,
            "four": 4,
            "five": 5,
            "six": 6,
            "seven": 7,
            "eight": 8,
            "nine": 9,
            "ten": 10
        }

        # Avoid phrases like "lives like a two-bedroom"
        if re.search(
            r"lives?\s+like\s+(?:a\s+)?(?:one|two|three|four|five|\d+)[- ]bedroom",
            text,
            re.IGNORECASE
        ):
            return None

        patterns = [
            r"(\d+(?:\.\d+)?)\s+(?:spacious\s+)?bedrooms?\b",
            r"(\d+(?:\.\d+)?)\s*[- ]?\s*bedrooms?\b",
            r"(\d+(?:\.\d+)?)\s*[- ]?\s*bed\b",
            r"(\d+(?:\.\d+)?)\s*[- ]?\s*br\b",
            r"(\d+(?:\.\d+)?)\s*[- ]?\s*bd\b"
        ]

        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return float(match.group(1))

        word_match = re.search(
            r"\b(one|two|three|four|five|six|seven|eight|nine|ten)"
            r"\s*[- ]?\s*bedrooms?\b",
            text,
            re.IGNORECASE
        )

        if word_match:
            return float(
                word_numbers[word_match.group(1).lower()]
            )

        return None

    def extract_bathrooms(self, text):
        word_numbers = {
            "one": 1,
            "two": 2,
            "three": 3,
            "four": 4,
            "five": 5,
            "six": 6,
            "seven": 7,
            "eight": 8,
            "nine": 9,
            "ten": 10
        }

        full_half_match = re.search(
            r"(\d+)\s+full\s+(?:bathrooms?|baths?)"
            r".{0,20}?"
            r"1/2\s+(?:bathrooms?|baths?)",
            text,
            re.IGNORECASE
        )

        if full_half_match:
            return float(full_half_match.group(1)) + 0.5

        fraction_match = re.search(
            r"(\d+)\s+1/2\s*[- ]?\s*(?:bathrooms?|baths?)\b",
            text,
            re.IGNORECASE
        )

        if fraction_match:
            return float(fraction_match.group(1)) + 0.5

        patterns = [
            r"(\d+(?:\.\d+)?)\s+(?:full\s+)?bathrooms?\b",
            r"(\d+(?:\.\d+)?)\s*[- ]?\s*bathrooms?\b",
            r"(\d+(?:\.\d+)?)\s*[- ]?\s*baths?\b",
            r"(\d+(?:\.\d+)?)\s*[- ]?\s*ba\b"
        ]

        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return float(match.group(1))

        word_match = re.search(
            r"\b(one|two|three|four|five|six|seven|eight|nine|ten)"
            r"\s*[- ]?\s*(?:bathrooms?|baths?)\b",
            text,
            re.IGNORECASE
        )

        if word_match:
            return float(
                word_numbers[word_match.group(1).lower()]
            )

        return None

    def extract_price(self, text):
        range_match = re.search(
            r"\$\s*([\d,]+)\s*-\s*\$?\s*([\d,]+)",
            text,
            re.IGNORECASE
        )

        if range_match:
            return int(
                range_match.group(1).replace(",", "")
            )

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
                return int(
                    match.group(1).replace(",", "")
                )

        return None

    def extract_sqft(self, text):
        living_patterns = [
            r"(\d[\d,]*)\s*-\s*square-foot\b",
            r"(\d[\d,]*)\s*\+\s*sq\.?\s*ft\.?\b",

            r"(?:offers?|offering|features?|approximately|approx\.?)\s*"
            r"(\d[\d,]*)\s*(?:square feet|sq\.?\s*ft\.?|sqft|sf)\s*"
            r"(?:of\s+)?(?:living|comfortable|thoughtfully designed)?\s*space",

            r"(\d[\d,]*)\s*(?:square feet|sq\.?\s*ft\.?|sqft|sf)\s*"
            r"of\s+living\s+space"
        ]

        for pattern in living_patterns:
            match = re.search(
                pattern,
                text,
                re.IGNORECASE
            )

            if match:
                return int(
                    match.group(1).replace(",", "")
                )

        general_patterns = [
            r"(\d[\d,]*)\s*-\s*square-foot\b",
            r"(\d[\d,]*)\s*\+\s*sq\.?\s*ft\.?\b",
            r"(\d[\d,]*)\s*square feet\b",
            r"(\d[\d,]*)\s*sq\.?\s*ft\.?\b",
            r"(\d[\d,]*)\s*sqft\b",
            r"(\d[\d,]*)\s*sf\b"
        ]

        for pattern in general_patterns:
            for match in re.finditer(
                pattern,
                text,
                re.IGNORECASE
            ):
                end = match.end()

                following_text = text[end:end + 40].lower()

                if "lot" in following_text or "land" in following_text:
                    continue

                return int(
                    match.group(1).replace(",", "")
                )

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
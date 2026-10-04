import re
import unicodedata


class TextCleaner:
    def __init__(self):
        self.abbrev_map = {
            "br": "bedroom",
            "bd": "bedroom",
            "bdr": "bedroom",
            "bdrm": "bedroom",
            "ba": "bathroom",
            "bth": "bathroom",
            "bath": "bathroom",
            "sqft": "square feet",
            "sq ft": "square feet",
            "sf": "square feet",
            "w/": "with",
            "w/o": "without",
            "mbr": "master bedroom",
            "fp": "fireplace",
            "gar": "garage",
            "ac": "air conditioning",
            "a/c": "air conditioning",
            "hoa": "homeowners association",
            "apt": "apartment",
            "condo": "condominium",
            "yr": "year",
            "yrs": "years",
            "mo": "month",
            "mos": "months",
            "pkg": "parking",
            "prkg": "parking",
            "rm": "room",
            "lvl": "level",
            "flr": "floor",
            "kit": "kitchen",
            "lr": "living room",
            "dr": "dining room",
            "fam rm": "family room",
            "laund": "laundry"
        }

    def normalize_unicode(self, text):
        if not isinstance(text, str):
            return ""
        return unicodedata.normalize("NFKC", text)

    def remove_html(self, text):
        return re.sub(r"<[^>]+>", " ", text)

    def normalize_whitespace(self, text):
        return re.sub(r"\s+", " ", text).strip()

    def normalize_prices(self, text):
        text = re.sub(
            r"\$?(\d+(?:\.\d+)?)\s*[kK]\b",
            lambda m: str(int(float(m.group(1)) * 1000)),
            text
        )

        text = re.sub(
            r"\$?(\d+(?:\.\d+)?)\s*[mM]\b",
            lambda m: str(int(float(m.group(1)) * 1_000_000)),
            text
        )

        return text

    def normalize_measurements(self, text):
        # Examples: 2,000 sqft, 2000 sq ft
        text = re.sub(
            r"(\d[\d,]*)\s*(?:sq\.?\s*ft\.?|sqft)\b",
            lambda m: f"{m.group(1).replace(',', '')} square feet",
            text,
            flags=re.IGNORECASE
        )

        # Examples: 5,000-square-foot, 2500 square foot
        text = re.sub(
            r"(\d[\d,]*)[-\s]+square[-\s]+(?:foot|feet)\b",
            lambda m: f"{m.group(1).replace(',', '')} square feet",
            text,
            flags=re.IGNORECASE
        )

        return text

    def expand_abbreviations(self, text):
        # Handle bedroom abbreviations attached to numbers
        text = re.sub(
            r"(\d+)\s*(?:br|bd|bdr|bdrm)\b",
            r"\1 bedroom",
            text,
            flags=re.IGNORECASE
        )

        # Handle bathroom abbreviations attached to numbers
        text = re.sub(
            r"(\d+)\s*(?:ba|bth)\b",
            r"\1 bathroom",
            text,
            flags=re.IGNORECASE
        )

        # Handle all other abbreviations
        for abbreviation, replacement in sorted(
            self.abbrev_map.items(),
            key=lambda x: len(x[0]),
            reverse=True
        ):
            # Already handled these above
            if abbreviation in {"br", "bd", "bdr", "bdrm", "ba", "bth"}:
                continue

            pattern = rf"(?<![A-Za-z]){re.escape(abbreviation)}(?![A-Za-z])"

            text = re.sub(
                pattern,
                replacement,
                text,
                flags=re.IGNORECASE
            )

        return text

    def normalize_punctuation(self, text):
        text = text.replace("–", " - ")
        text = text.replace("—", " - ")
        text = text.replace("“", '"')
        text = text.replace("”", '"')
        text = text.replace("’", "'")
        return text

    def clean_text(self, text):
        text = self.normalize_unicode(text)
        text = self.remove_html(text)
        text = self.normalize_punctuation(text)
        text = self.normalize_prices(text)
        text = self.normalize_measurements(text)
        text = self.expand_abbreviations(text)
        text = self.normalize_sentence_spacing(text)
        text = self.normalize_whitespace(text)

        return text

    def normalize_sentence_spacing(self, text):
        text = re.sub(r"([.!?])([A-Za-z])", r"\1 \2", text)
        return text
    
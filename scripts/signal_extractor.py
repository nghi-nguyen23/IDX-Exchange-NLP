import json
import re

class SignalExtractor:
    def __init__(
        self,
        taxonomy_path="data/processed/taxonomy.json",
        entity_extractor=None
    ):
        with open(taxonomy_path, "r") as f:
            self.taxonomy = json.load(f)

        self.extractor = entity_extractor

        self.amenity_terms = [
            item["term"].lower()
            for item in self.taxonomy["terms"]
            if item["category"] in {
                "amenities",
                "property_features",
                "outdoor_features"
            }
        ]

        self.condition_terms = [
            "updated",
            "renovated",
            "remodeled",
            "new construction",
            "move-in ready",
            "turnkey"
        ]

        self.financing_terms = [
            "seller financing",
            "assumable loan",
            "cash only",
            "financing available"
        ]

        self.location_terms = [
            "near beach",
            "ocean view",
            "mountain view",
            "near shopping",
            "near dining",
            "freeway access",
            "near downtown",
            "walking distance",
            "gated community"
        ]

    def _match_terms(self, text, terms):
        text_lower = text.lower()

        return sorted({
            term
            for term in terms
            if re.search(
                rf"\b{re.escape(term)}\b",
                text_lower
            )
        })

    def _match_amenities(self, remarks):
        return self._match_terms(
            remarks,
            self.amenity_terms
        )

    def _extract_condition(self, remarks):
        return self._match_terms(
            remarks,
            self.condition_terms
        )

    def _extract_financing(self, remarks):
        return self._match_terms(
            remarks,
            self.financing_terms
        )

    def _extract_location(self, remarks):
        return self._match_terms(
            remarks,
            self.location_terms
        )

    def extract_signals(self, listing_record):
        remarks = listing_record.get("L_Remarks", "") or ""

        entities = {}

        if self.extractor is not None:
            entities = self.extractor.extract_all(remarks)

        return {
            "listing_id": listing_record.get("L_ListingID"),
            "entities": entities,
            "amenities": self._match_amenities(remarks),
            "condition_keywords": self._extract_condition(remarks),
            "financing_terms": self._extract_financing(remarks),
            "location_features": self._extract_location(remarks)
        }
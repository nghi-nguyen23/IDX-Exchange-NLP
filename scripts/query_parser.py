import re


class QueryParser:
    def __init__(self):
        self.amenities = [
            "pool",
            "garage",
            "fireplace",
            "patio",
            "spa",
            "solar",
            "backyard"
        ]

    def _parse_number(self, number, suffix=""):
        value = float(number)

        if suffix.lower() == "k":
            value *= 1000
        elif suffix.lower() == "m":
            value *= 1000000

        return int(value)

    def parse(self, query):
        filters = {}
        query_lower = query.lower()

        # PRICE
        price_between = re.search(
            r"between\s+\$?(\d+(?:\.\d+)?)([km]?)\s+(?:and|to)\s+\$?(\d+(?:\.\d+)?)([km]?)",
            query_lower
        )

        if price_between:
            filters["price_min"] = self._parse_number(
                price_between.group(1),
                price_between.group(2)
            )
            filters["price_max"] = self._parse_number(
                price_between.group(3),
                price_between.group(4)
            )

        else:
            price_max_patterns = [
                r"under\s+\$?(\d+(?:\.\d+)?)([km]?)",
                r"below\s+\$?(\d+(?:\.\d+)?)([km]?)",
                r"less than\s+\$?(\d+(?:\.\d+)?)([km]?)",
                r"up to\s+\$?(\d+(?:\.\d+)?)([km]?)",
                r"max(?:imum)?\s+\$?(\d+(?:\.\d+)?)([km]?)"
            ]

            for pattern in price_max_patterns:
                match = re.search(pattern, query_lower)
                if match:
                    filters["price_max"] = self._parse_number(
                        match.group(1),
                        match.group(2)
                    )
                    break

            price_min_patterns = [
                r"over\s+\$?(\d+(?:\.\d+)?)([km]?)",
                r"above\s+\$?(\d+(?:\.\d+)?)([km]?)",
                r"more than\s+\$?(\d+(?:\.\d+)?)([km]?)",
                r"at least\s+\$?(\d+(?:\.\d+)?)([km]?)",
                r"minimum\s+\$?(\d+(?:\.\d+)?)([km]?)"
            ]

            for pattern in price_min_patterns:
                match = re.search(pattern, query_lower)
                if match:
                    filters["price_min"] = self._parse_number(
                        match.group(1),
                        match.group(2)
                    )
                    break

        # BEDROOMS
        bed_between = re.search(
            r"between\s+(\d+)\s+(?:and|to)\s+(\d+)\s*(?:bed|beds|bedroom|bedrooms)",
            query_lower
        )

        if bed_between:
            filters["bedrooms_min"] = int(bed_between.group(1))
            filters["bedrooms_max"] = int(bed_between.group(2))

        else:
            bed_min = re.search(
                r"(\d+)\+\s*(?:bed|beds|bedroom|bedrooms)",
                query_lower
            )

            if not bed_min:
                bed_min = re.search(
                    r"at least\s+(\d+)\s*(?:bed|beds|bedroom|bedrooms)",
                    query_lower
                )

            if bed_min:
                filters["bedrooms_min"] = int(bed_min.group(1))

            else:
                bed_exact = re.search(
                    r"(\d+)\s*(?:bed|beds|bedroom|bedrooms|br)\b",
                    query_lower
                )

                if bed_exact:
                    filters["bedrooms"] = int(bed_exact.group(1))

        bed_max = re.search(
            r"(?:up to|maximum|max)\s+(\d+)\s*(?:bed|beds|bedroom|bedrooms)",
            query_lower
        )

        if bed_max:
            filters["bedrooms_max"] = int(bed_max.group(1))

        # BATHROOMS
        bath_between = re.search(
            r"between\s+(\d+(?:\.\d+)?)\s+(?:and|to)\s+(\d+(?:\.\d+)?)\s*(?:bath|baths|bathroom|bathrooms)",
            query_lower
        )

        if bath_between:
            filters["bathrooms_min"] = float(bath_between.group(1))
            filters["bathrooms_max"] = float(bath_between.group(2))

        else:
            bath_min = re.search(
                r"(\d+(?:\.\d+)?)\+\s*(?:bath|baths|bathroom|bathrooms)",
                query_lower
            )

            if not bath_min:
                bath_min = re.search(
                    r"at least\s+(\d+(?:\.\d+)?)\s*(?:bath|baths|bathroom|bathrooms)",
                    query_lower
                )

            if bath_min:
                filters["bathrooms_min"] = float(bath_min.group(1))

            else:
                bath_exact = re.search(
                    r"(\d+(?:\.\d+)?)\s*(?:bath|baths|bathroom|bathrooms|ba)\b",
                    query_lower
                )

                if bath_exact:
                    filters["bathrooms"] = float(bath_exact.group(1))

        bath_max = re.search(
            r"(?:up to|maximum|max)\s+(\d+(?:\.\d+)?)\s*(?:bath|baths|bathroom|bathrooms)",
            query_lower
        )

        if bath_max:
            filters["bathrooms_max"] = float(bath_max.group(1))

      
        # CITY
        city_match = re.search(
            r"\bin\s+([a-zA-Z\s]+?)(?=\s+(?:under|below|over|above|with|without|at least|between)|$)",
            query,
            re.IGNORECASE
        )

        if city_match:
            filters["city"] = city_match.group(1).strip().title()

    
        # AMENITIES + NEGATION
        amenities = []
        excluded_amenities = []

        for amenity in self.amenities:
            if re.search(
                rf"\b(?:without|no)\s+(?:a\s+)?{re.escape(amenity)}\b",
                query_lower
            ):
                excluded_amenities.append(amenity)

            elif re.search(
                rf"\b{re.escape(amenity)}\b",
                query_lower
            ):
                amenities.append(amenity)

        if amenities:
            filters["amenities"] = amenities

        if excluded_amenities:
            filters["exclude_amenities"] = excluded_amenities

        return filters

    def to_sql(self, filters):
        conditions = []
        params = []

        if "price_min" in filters:
            conditions.append("L_SystemPrice >= %s")
            params.append(filters["price_min"])

        if "price_max" in filters:
            conditions.append("L_SystemPrice <= %s")
            params.append(filters["price_max"])

        if "bedrooms" in filters:
            conditions.append("L_Keyword2 = %s")
            params.append(filters["bedrooms"])

        if "bedrooms_min" in filters:
            conditions.append("L_Keyword2 >= %s")
            params.append(filters["bedrooms_min"])

        if "bedrooms_max" in filters:
            conditions.append("L_Keyword2 <= %s")
            params.append(filters["bedrooms_max"])

        if "bathrooms" in filters:
            conditions.append("LM_Dec_3 = %s")
            params.append(filters["bathrooms"])

        if "bathrooms_min" in filters:
            conditions.append("LM_Dec_3 >= %s")
            params.append(filters["bathrooms_min"])

        if "bathrooms_max" in filters:
            conditions.append("LM_Dec_3 <= %s")
            params.append(filters["bathrooms_max"])

        if "city" in filters:
            conditions.append("L_City = %s")
            params.append(filters["city"])

        for amenity in filters.get("amenities", []):
            conditions.append("L_Remarks LIKE %s")
            params.append(f"%{amenity}%")

        for amenity in filters.get("exclude_amenities", []):
            conditions.append("L_Remarks NOT LIKE %s")
            params.append(f"%{amenity}%")

        where_clause = " AND ".join(conditions)

        if where_clause:
            sql = f"SELECT * FROM rets_property WHERE {where_clause}"
        else:
            sql = "SELECT * FROM rets_property"

        return sql, params
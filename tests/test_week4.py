import pytest

from scripts.query_parser import QueryParser, SchemaValidator


parser = QueryParser()


@pytest.mark.parametrize(
    "query, expected",
    [
        # PRICE MAX
        ("homes under 500k", {"price_max": 500000}),
        ("homes below 600k", {"price_max": 600000}),
        ("homes less than 700k", {"price_max": 700000}),
        ("homes up to 800k", {"price_max": 800000}),

        # PRICE MIN
        ("homes over 500k", {"price_min": 500000}),
        ("homes above 600k", {"price_min": 600000}),
        ("homes more than 700k", {"price_min": 700000}),
        ("homes at least 800k", {"price_min": 800000}),

        # PRICE RANGE
        (
            "homes between 500k and 700k",
            {"price_min": 500000, "price_max": 700000},
        ),
        (
            "homes between 1m and 1.5m",
            {"price_min": 1000000, "price_max": 1500000},
        ),

        # BEDROOM EXACT
        ("3 bed homes", {"bedrooms": 3}),
        ("4 beds", {"bedrooms": 4}),
        ("2 bedroom homes", {"bedrooms": 2}),
        ("3 br homes", {"bedrooms": 3}),

        # BEDROOM MIN
        ("3+ beds", {"bedrooms_min": 3}),
        ("4+ bedrooms", {"bedrooms_min": 4}),
        ("at least 2 bedrooms", {"bedrooms_min": 2}),

        # BEDROOM MAX
        ("up to 4 bedrooms", {"bedrooms_max": 4}),
        ("maximum 5 beds", {"bedrooms_max": 5}),
        ("max 3 bedrooms", {"bedrooms_max": 3}),

        # BEDROOM RANGE
        (
            "between 2 and 4 bedrooms",
            {"bedrooms_min": 2, "bedrooms_max": 4},
        ),
        (
            "between 3 to 5 beds",
            {"bedrooms_min": 3, "bedrooms_max": 5},
        ),

        # BATHROOM EXACT
        ("2 bath homes", {"bathrooms": 2.0}),
        ("3 baths", {"bathrooms": 3.0}),
        ("2.5 bathrooms", {"bathrooms": 2.5}),

        # BATHROOM MIN
        ("2+ baths", {"bathrooms_min": 2.0}),
        ("2.5+ bathrooms", {"bathrooms_min": 2.5}),
        ("at least 2 baths", {"bathrooms_min": 2.0}),

        # BATHROOM MAX
        ("up to 3 bathrooms", {"bathrooms_max": 3.0}),
        ("maximum 2 baths", {"bathrooms_max": 2.0}),
        ("max 2.5 bathrooms", {"bathrooms_max": 2.5}),

        # BATHROOM RANGE
        (
            "between 2 and 3 bathrooms",
            {"bathrooms_min": 2.0, "bathrooms_max": 3.0},
        ),
        (
            "between 1.5 to 2.5 baths",
            {"bathrooms_min": 1.5, "bathrooms_max": 2.5},
        ),

        # CITY
        ("homes in Irvine", {"city": "Irvine"}),
        ("homes in San Diego", {"city": "San Diego"}),
        ("homes in Riverside", {"city": "Riverside"}),

        # AMENITIES
        ("homes with pool", {"amenities": ["pool"]}),
        ("homes with garage", {"amenities": ["garage"]}),
        ("homes with fireplace", {"amenities": ["fireplace"]}),
        ("homes with spa", {"amenities": ["spa"]}),

        # NEGATION
        ("homes without pool", {"exclude_amenities": ["pool"]}),
        ("homes no garage", {"exclude_amenities": ["garage"]}),

        # COMBINED
        (
            "3 bed under 700k in Irvine with pool",
            {
                "price_max": 700000,
                "bedrooms": 3,
                "city": "Irvine",
                "amenities": ["pool"],
            },
        ),
        (
            "4+ bedrooms over 1m in San Diego with garage",
            {
                "price_min": 1000000,
                "bedrooms_min": 4,
                "city": "San Diego",
                "amenities": ["garage"],
            },
        ),
    ],
)
def test_query_parser(query, expected):
    assert parser.parse(query) == expected


def test_sql_generation():
    filters = {
        "bedrooms": 3,
        "price_max": 700000,
        "city": "Irvine",
    }

    sql, params = parser.to_sql(filters)

    assert "L_Keyword2 = %s" in sql
    assert "L_SystemPrice <= %s" in sql
    assert "L_City = %s" in sql
    assert params == [700000, 3, "Irvine"]


def test_sql_injection_city():
    filters = {
        "city": "Irvine'; DROP TABLE rets_property; --"
    }

    sql, params = parser.to_sql(filters)

    assert "DROP TABLE" not in sql
    assert params == ["Irvine'; DROP TABLE rets_property; --"]


def test_sql_injection_amenity():
    filters = {
        "amenities": ["pool'; DROP TABLE rets_property; --"]
    }

    sql, params = parser.to_sql(filters)

    assert "DROP TABLE" not in sql
    assert params == ["%pool'; DROP TABLE rets_property; --%"]


@pytest.fixture
def validator():
    return SchemaValidator()


def test_valid_city(validator):
    valid, errors = validator.validate_query({
        "city": "San Diego"
    })

    assert valid is True
    assert errors == []


def test_invalid_city(validator):
    valid, errors = validator.validate_query({
        "city": "Fake City"
    })

    assert valid is False


def test_invalid_price_low(validator):
    valid, errors = validator.validate_query({
        "price_max": 50000
    })

    assert valid is False


def test_invalid_price_high(validator):
    valid, errors = validator.validate_query({
        "price_max": 20000000
    })

    assert valid is False


def test_invalid_bedrooms(validator):
    valid, errors = validator.validate_query({
        "bedrooms": 25
    })

    assert valid is False
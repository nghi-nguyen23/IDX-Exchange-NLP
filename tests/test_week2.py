import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from scripts.text_cleaning import TextCleaner

cleaner = TextCleaner()


# -------------------------
# Unicode / punctuation
# -------------------------

def test_unicode_normalization():
    assert cleaner.normalize_unicode("café") == "café"


def test_em_dash():
    assert cleaner.clean_text("open—concept") == "open - concept"


def test_en_dash():
    assert cleaner.clean_text("indoor–outdoor") == "indoor - outdoor"


def test_curly_apostrophe():
    assert cleaner.clean_text("seller’s home") == "seller's home"


def test_curly_quotes():
    assert cleaner.clean_text('“luxury home”') == '"luxury home"'


# -------------------------
# HTML
# -------------------------

def test_remove_html_paragraph():
    assert cleaner.clean_text("<p>Beautiful home</p>") == "Beautiful home"


def test_remove_html_bold():
    assert cleaner.clean_text("<b>Updated kitchen</b>") == "Updated kitchen"


def test_remove_multiple_html_tags():
    assert cleaner.clean_text("<div><p>Pool home</p></div>") == "Pool home"


# -------------------------
# Whitespace
# -------------------------

def test_extra_spaces():
    assert cleaner.clean_text("Beautiful   home") == "Beautiful home"


def test_newlines():
    assert cleaner.clean_text("Beautiful\nhome") == "Beautiful home"


def test_tabs():
    assert cleaner.clean_text("Beautiful\thome") == "Beautiful home"


def test_leading_spaces():
    assert cleaner.clean_text("   Beautiful home") == "Beautiful home"


def test_trailing_spaces():
    assert cleaner.clean_text("Beautiful home   ") == "Beautiful home"


# -------------------------
# Price normalization
# -------------------------

def test_price_450k():
    assert cleaner.normalize_prices("450k") == "450000"


def test_price_uppercase_k():
    assert cleaner.normalize_prices("850K") == "850000"


def test_price_with_dollar_k():
    assert cleaner.normalize_prices("$500k") == "500000"


def test_price_1m():
    assert cleaner.normalize_prices("1m") == "1000000"


def test_price_1_2m():
    assert cleaner.normalize_prices("1.2m") == "1200000"


def test_price_with_dollar_m():
    assert cleaner.normalize_prices("$2.5M") == "2500000"


def test_price_in_sentence():
    result = cleaner.clean_text("Priced at $1.2M")
    assert "1200000" in result


# -------------------------
# Measurement normalization
# -------------------------

def test_sqft():
    assert cleaner.clean_text("2000 sqft") == "2000 square feet"


def test_sq_ft():
    assert cleaner.clean_text("2000 sq ft") == "2000 square feet"


def test_sqft_with_comma():
    assert cleaner.clean_text("2,000 sqft") == "2000 square feet"


def test_square_foot_hyphenated():
    assert cleaner.clean_text("5,000-square-foot") == "5000 square feet"


def test_square_foot_space():
    assert cleaner.clean_text("2500 square foot") == "2500 square feet"


# -------------------------
# Bedroom abbreviations
# -------------------------

def test_br():
    assert cleaner.clean_text("3BR") == "3 bedroom"


def test_bd():
    assert cleaner.clean_text("4BD") == "4 bedroom"


def test_bdr():
    assert cleaner.clean_text("2BDR") == "2 bedroom"


def test_bdrm():
    assert cleaner.clean_text("5BDRM") == "5 bedroom"


# -------------------------
# Bathroom abbreviations
# -------------------------

def test_ba():
    assert cleaner.clean_text("2BA") == "2 bathroom"


def test_bth():
    assert cleaner.clean_text("3BTH") == "3 bathroom"


def test_bath_word():
    assert cleaner.clean_text("private bath") == "private bathroom"


# -------------------------
# Other abbreviations
# -------------------------

def test_with():
    assert cleaner.clean_text("home w/ pool") == "home with pool"


def test_without():
    assert cleaner.clean_text("unit w/o garage") == "unit without garage"


def test_mbr():
    assert cleaner.clean_text("large MBR") == "large master bedroom"


def test_fp():
    assert cleaner.clean_text("stone FP") == "stone fireplace"


def test_garage():
    assert cleaner.clean_text("2 car gar") == "2 car garage"


def test_ac():
    assert cleaner.clean_text("central AC") == "central air conditioning"


def test_a_c():
    assert cleaner.clean_text("new A/C") == "new air conditioning"


def test_hoa():
    assert cleaner.clean_text("low HOA") == "low homeowners association"


def test_apt():
    assert cleaner.clean_text("1BR apt") == "1 bedroom apartment"


def test_condo():
    assert cleaner.clean_text("luxury condo") == "luxury condominium"


def test_room():
    assert cleaner.clean_text("bonus rm") == "bonus room"


def test_floor():
    assert cleaner.clean_text("second flr") == "second floor"


def test_kitchen():
    assert cleaner.clean_text("updated kit") == "updated kitchen"


def test_living_room():
    assert cleaner.clean_text("large LR") == "large living room"


def test_dining_room():
    assert cleaner.clean_text("formal DR") == "formal dining room"


# -------------------------
# Sentence spacing
# -------------------------

def test_missing_space_after_period():
    assert cleaner.clean_text("garage.A true gem") == "garage. A true gem"


def test_missing_space_after_exclamation():
    assert cleaner.clean_text("Amazing!Must see") == "Amazing! Must see"


def test_missing_space_after_question():
    assert cleaner.clean_text("Interested?Call today") == "Interested? Call today"


# -------------------------
# General / edge cases
# -------------------------

def test_empty_string():
    assert cleaner.clean_text("") == ""


def test_none():
    assert cleaner.clean_text(None) == ""


def test_full_example():
    result = cleaner.clean_text(
        "<p>Beautiful 3BR w/ 2BA, 2,000 sqft, priced at $850K!</p>"
    )

    assert "3 bedroom" in result
    assert "2 bathroom" in result
    assert "2000 square feet" in result
    assert "850000" in result
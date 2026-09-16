from src.tools import check_char_limits, check_tag_diversity


def test_check_char_limits_flags_long_tag():
    result = check_char_limits(
        "Short title",
        ["a fine short tag", "this tag is definitely way too long for etsy"],
    )
    assert result["bad_tags"] == ["this tag is definitely way too long for etsy"]


def test_check_char_limits_flags_too_many_tags():
    result = check_char_limits("Title", ["tag"] * 14)
    assert result["tag_count_ok"] is False


def test_check_char_limits_all_ok():
    result = check_char_limits("Handmade walnut cutting board", ["walnut", "kitchen"])
    assert result["title_ok"] is True
    assert result["tag_count_ok"] is True
    assert result["bad_tags"] == []


def test_check_tag_diversity_flags_repeated_word():
    result = check_tag_diversity(["walnut board", "walnut coasters"])
    assert result["duplicated_word_tags"] == ["walnut coasters"]


def test_check_tag_diversity_no_repeats():
    result = check_tag_diversity(["walnut board", "kitchen decor"])
    assert result["duplicated_word_tags"] == []

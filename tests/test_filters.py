from x_scraper.filters import KeywordMatcher


def test_include_keyword_match():
    m = KeywordMatcher(include=["AI"], exclude=[])
    result = m.evaluate("This is an ai update")
    assert result.matched
    assert result.keywords == ["AI"]


def test_exclude_wins():
    m = KeywordMatcher(include=["AI"], exclude=["ban"])
    result = m.evaluate("AI ban debate")
    assert not result.matched


def test_regex_mode():
    m = KeywordMatcher(include=[r"AI\s+model"], exclude=[], regex_mode=True)
    result = m.evaluate("New AI model released")
    assert result.matched

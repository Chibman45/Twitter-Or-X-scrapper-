from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass(slots=True)
class MatchResult:
    matched: bool
    keywords: list[str]


class KeywordMatcher:
    def __init__(self, include: list[str], exclude: list[str], regex_mode: bool = False):
        self.include = include
        self.exclude = exclude
        self.regex_mode = regex_mode

    def _matches(self, text: str, pattern: str) -> bool:
        if self.regex_mode:
            return re.search(pattern, text, flags=re.IGNORECASE) is not None
        return pattern.lower() in text.lower()

    def evaluate(self, text: str) -> MatchResult:
        if any(self._matches(text, pat) for pat in self.exclude):
            return MatchResult(False, [])

        if not self.include:
            return MatchResult(True, [])

        hits = [pat for pat in self.include if self._matches(text, pat)]
        return MatchResult(bool(hits), hits)

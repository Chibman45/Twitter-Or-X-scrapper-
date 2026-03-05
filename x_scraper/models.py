from __future__ import annotations

from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from typing import Any


@dataclass(slots=True)
class TweetRecord:
    tweet_id: str
    account_handle: str
    tweet_url: str
    created_at: str
    text: str
    language: str | None
    is_reply: bool
    is_repost: bool
    hashtags: list[str]
    mentions: list[str]
    like_count: int | None
    reply_count: int | None
    repost_count: int | None
    view_count: int | None
    matched_keywords: list[str]
    ingested_at: str
    source_run_id: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()

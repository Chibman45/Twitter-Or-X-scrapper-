from __future__ import annotations

from dataclasses import dataclass
from uuid import uuid4

import snscrape.modules.twitter as sntwitter

from .checkpoint import CheckpointStore
from .filters import KeywordMatcher
from .models import TweetRecord, now_iso
from .storage import StorageWriter


@dataclass(slots=True)
class RunSummary:
    fetched: int = 0
    matched: int = 0
    written: int = 0


class AccountKeywordScraper:
    def __init__(
        self,
        matcher: KeywordMatcher,
        checkpoint: CheckpointStore,
        storage: StorageWriter,
        max_tweets_per_account: int = 100,
    ):
        self.matcher = matcher
        self.checkpoint = checkpoint
        self.storage = storage
        self.max_tweets_per_account = max_tweets_per_account

    def run(self, accounts: list[str]) -> RunSummary:
        run_id = str(uuid4())
        summary = RunSummary()

        for account in accounts:
            last_seen = self.checkpoint.get_last_seen(account)
            matched_records: list[TweetRecord] = []

            for idx, tweet in enumerate(sntwitter.TwitterUserScraper(account).get_items()):
                if idx >= self.max_tweets_per_account:
                    break
                summary.fetched += 1

                tid = str(tweet.id)
                if last_seen is not None and int(tid) <= int(last_seen):
                    continue

                result = self.matcher.evaluate(tweet.rawContent or "")
                if not result.matched:
                    continue

                summary.matched += 1
                rec = TweetRecord(
                    tweet_id=tid,
                    account_handle=account,
                    tweet_url=tweet.url,
                    created_at=tweet.date.isoformat(),
                    text=tweet.rawContent or "",
                    language=getattr(tweet, "lang", None),
                    is_reply=tweet.inReplyToTweetId is not None,
                    is_repost=tweet.retweetedTweet is not None,
                    hashtags=tweet.hashtags or [],
                    mentions=[u.username for u in (tweet.mentionedUsers or [])],
                    like_count=getattr(tweet, "likeCount", None),
                    reply_count=getattr(tweet, "replyCount", None),
                    repost_count=getattr(tweet, "retweetCount", None),
                    view_count=getattr(tweet, "viewCount", None),
                    matched_keywords=result.keywords,
                    ingested_at=now_iso(),
                    source_run_id=run_id,
                )
                matched_records.append(rec)
                self.checkpoint.set_last_seen(account, tid)

            summary.written += self.storage.write(matched_records)

        return summary

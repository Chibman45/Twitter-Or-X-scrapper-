from __future__ import annotations

import csv
import json
import sqlite3
from pathlib import Path

from .models import TweetRecord


class StorageWriter:
    def __init__(self, jsonl_path: str, csv_path: str, sqlite_path: str | None):
        self.jsonl_path = Path(jsonl_path)
        self.csv_path = Path(csv_path)
        self.sqlite_path = Path(sqlite_path) if sqlite_path else None

        self.jsonl_path.parent.mkdir(parents=True, exist_ok=True)
        self.csv_path.parent.mkdir(parents=True, exist_ok=True)
        if self.sqlite_path:
            self.sqlite_path.parent.mkdir(parents=True, exist_ok=True)
            self._init_db()

    def _init_db(self) -> None:
        assert self.sqlite_path
        with sqlite3.connect(self.sqlite_path) as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS tweets (
                    tweet_id TEXT NOT NULL,
                    account_handle TEXT NOT NULL,
                    payload_json TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    PRIMARY KEY (tweet_id, account_handle)
                )
                """
            )

    def write(self, records: list[TweetRecord]) -> int:
        if not records:
            return 0

        fieldnames = list(records[0].to_dict().keys())

        with self.jsonl_path.open("a", encoding="utf-8") as jf:
            for rec in records:
                jf.write(json.dumps(rec.to_dict(), ensure_ascii=False) + "\n")

        csv_exists = self.csv_path.exists() and self.csv_path.stat().st_size > 0
        with self.csv_path.open("a", encoding="utf-8", newline="") as cf:
            writer = csv.DictWriter(cf, fieldnames=fieldnames)
            if not csv_exists:
                writer.writeheader()
            for rec in records:
                row = rec.to_dict()
                row["hashtags"] = ",".join(row["hashtags"])
                row["mentions"] = ",".join(row["mentions"])
                row["matched_keywords"] = ",".join(row["matched_keywords"])
                writer.writerow(row)

        if self.sqlite_path:
            with sqlite3.connect(self.sqlite_path) as conn:
                for rec in records:
                    payload = rec.to_dict()
                    conn.execute(
                        """
                        INSERT OR IGNORE INTO tweets (tweet_id, account_handle, payload_json, created_at)
                        VALUES (?, ?, ?, ?)
                        """,
                        (rec.tweet_id, rec.account_handle, json.dumps(payload, ensure_ascii=False), rec.created_at),
                    )

        return len(records)

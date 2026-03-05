from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import yaml


@dataclass(slots=True)
class KeywordConfig:
    include: list[str]
    exclude: list[str]
    regex_mode: bool = False


@dataclass(slots=True)
class ExportConfig:
    jsonl_path: str = "output/tweets.jsonl"
    csv_path: str = "output/tweets.csv"


@dataclass(slots=True)
class StorageConfig:
    sqlite_path: str | None = "output/tweets.db"
    checkpoint_path: str = "output/checkpoints.json"


@dataclass(slots=True)
class RuntimeConfig:
    max_tweets_per_account: int = 100


@dataclass(slots=True)
class AppConfig:
    accounts: list[str]
    keywords: KeywordConfig
    export: ExportConfig
    storage: StorageConfig
    runtime: RuntimeConfig


DEFAULTS = {
    "accounts": [],
    "keywords": {"include": [], "exclude": [], "regex_mode": False},
    "export": {"jsonl_path": "output/tweets.jsonl", "csv_path": "output/tweets.csv"},
    "storage": {"sqlite_path": "output/tweets.db", "checkpoint_path": "output/checkpoints.json"},
    "runtime": {"max_tweets_per_account": 100},
}


def load_config(path: str) -> AppConfig:
    payload = yaml.safe_load(Path(path).read_text()) or {}
    merged = DEFAULTS | payload
    merged["keywords"] = DEFAULTS["keywords"] | (payload.get("keywords") or {})
    merged["export"] = DEFAULTS["export"] | (payload.get("export") or {})
    merged["storage"] = DEFAULTS["storage"] | (payload.get("storage") or {})
    merged["runtime"] = DEFAULTS["runtime"] | (payload.get("runtime") or {})

    accounts = [a.strip().lstrip("@") for a in merged["accounts"] if str(a).strip()]
    if not accounts:
        raise ValueError("Config must include at least one account.")

    return AppConfig(
        accounts=accounts,
        keywords=KeywordConfig(**merged["keywords"]),
        export=ExportConfig(**merged["export"]),
        storage=StorageConfig(**merged["storage"]),
        runtime=RuntimeConfig(**merged["runtime"]),
    )

from __future__ import annotations

import argparse
import json
import logging

from .checkpoint import CheckpointStore
from .config import load_config
from .filters import KeywordMatcher
from .scraper import AccountKeywordScraper
from .storage import StorageWriter


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="X account keyword scraper")
    parser.add_argument("--config", default="config.yaml", help="Path to YAML config")
    return parser


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    args = build_parser().parse_args()
    cfg = load_config(args.config)

    matcher = KeywordMatcher(
        include=cfg.keywords.include,
        exclude=cfg.keywords.exclude,
        regex_mode=cfg.keywords.regex_mode,
    )
    checkpoint = CheckpointStore(cfg.storage.checkpoint_path)
    storage = StorageWriter(
        jsonl_path=cfg.export.jsonl_path,
        csv_path=cfg.export.csv_path,
        sqlite_path=cfg.storage.sqlite_path,
    )

    app = AccountKeywordScraper(
        matcher=matcher,
        checkpoint=checkpoint,
        storage=storage,
        max_tweets_per_account=cfg.runtime.max_tweets_per_account,
    )
    summary = app.run(cfg.accounts)
    print(json.dumps(summary.__dict__, indent=2))


if __name__ == "__main__":
    main()

# X (Twitter) Account + Keyword Scraper

A Python project that scrapes posts from target X accounts and filters them by keyword rules.

This implementation combines:
- **Version 1 focus**: account targeting, keyword filtering, extraction, incremental sync, and export.
- **Version 4 focus**: verification-ready structure with unit tests for core logic.

## Features
- Scrape one or more accounts.
- Include/exclude keyword filtering (case-insensitive).
- Optional regex keyword mode.
- Incremental fetch via per-account checkpoint file.
- Export to JSONL, CSV, and optional SQLite.
- Simple CLI entrypoint with YAML config.

## Project Structure
- `x_scraper/config.py` — config loading and validation.
- `x_scraper/scraper.py` — orchestration and scraping pipeline.
- `x_scraper/filters.py` — keyword matching logic.
- `x_scraper/checkpoint.py` — incremental checkpoint storage.
- `x_scraper/storage.py` — JSONL/CSV/SQLite output writers.
- `x_scraper/cli.py` — command-line interface.
- `tests/` — unit tests.

## Quickstart
```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
cp config.example.yaml config.yaml
x-scraper --config config.yaml
```

## Configuration
Use `config.example.yaml` as a template:
- `accounts`: handles without `@`
- `keywords.include`: required keyword matches (or empty for all)
- `keywords.exclude`: blacklist terms
- `keywords.regex_mode`: use regex matching
- `runtime.max_tweets_per_account`: cap per account per run
- `storage.checkpoint_path`: per-account last-seen tweet IDs

## Tests
```bash
pytest
```

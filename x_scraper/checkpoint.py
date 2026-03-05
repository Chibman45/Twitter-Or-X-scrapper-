from __future__ import annotations

import json
from pathlib import Path


class CheckpointStore:
    def __init__(self, path: str):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if not self.path.exists():
            self.path.write_text("{}")

    def load(self) -> dict[str, str]:
        return json.loads(self.path.read_text() or "{}")

    def get_last_seen(self, account: str) -> str | None:
        return self.load().get(account)

    def set_last_seen(self, account: str, tweet_id: str) -> None:
        data = self.load()
        current = data.get(account)
        if current is None or int(tweet_id) > int(current):
            data[account] = tweet_id
            self.path.write_text(json.dumps(data, indent=2, sort_keys=True))

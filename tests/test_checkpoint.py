from x_scraper.checkpoint import CheckpointStore


def test_checkpoint_monotonic(tmp_path):
    p = tmp_path / "ckpt.json"
    store = CheckpointStore(str(p))
    store.set_last_seen("nasa", "100")
    store.set_last_seen("nasa", "99")
    assert store.get_last_seen("nasa") == "100"
    store.set_last_seen("nasa", "120")
    assert store.get_last_seen("nasa") == "120"

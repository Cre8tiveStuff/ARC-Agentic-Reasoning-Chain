from arc import idempotent

call_count = {"n": 0}

@idempotent
def do_work(name):
    call_count["n"] += 1
    return {"status": "done", "name": name}

def test_idempotent_runs_once_on_first_call():
    result = do_work("test_a")
    assert result["status"] == "done"

def test_idempotent_skips_duplicate_call():
    call_count["n"] = 0
    do_work("test_b")
    result = do_work("test_b")
    assert result["status"] == "skipped"
    assert call_count["n"] == 1
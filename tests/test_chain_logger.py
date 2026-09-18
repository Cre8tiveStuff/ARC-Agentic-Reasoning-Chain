from chain_logger import new_run_id, log_step, get_chain

def test_chain_logs_steps_in_order():
    run_id = new_run_id()
    log_step(run_id, 1, "refresh_index")
    log_step(run_id, 2, "answer_question")

    chain = get_chain(run_id)

    assert len(chain) == 2
    assert chain[0][1] == "refresh_index"
    assert chain[1][1] == "answer_question"
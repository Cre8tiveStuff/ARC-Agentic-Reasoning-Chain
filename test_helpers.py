def assert_tool_order(agent_result, expected_order):
    messages = agent_result.get("messages", [])
    actual_calls = []

    for msg in messages:
        tool_calls = getattr(msg, "tool_calls", None)
        if tool_calls:
            for call in tool_calls:
                actual_calls.append(call["name"])

    assert actual_calls == expected_order, (
        f"Expected tool call order {expected_order}, got {actual_calls}"
    )
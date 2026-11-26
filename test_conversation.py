
from unittest.mock import patch

from Agent.memory import ConversationMemory
from Agent.llm import ask_llm


memory = ConversationMemory()

# Simulate a successful response.
with patch(
    "Agent.llm.generate_with_fallback",
    return_value="Recursion is when a function calls itself."
) as mock_router:

    answer = ask_llm("Explain recursion.", memory)

assert len(memory.get_history()) == 2

print("PASS: Successful exchange saved.")

# Simulate a total API failure.
with patch(
    "Agent.llm.generate_with_fallback",
    side_effect=RuntimeError("All models unavailable")
):
    try:
        ask_llm("Give me an example.", memory)
    except RuntimeError:
        pass

assert len(memory.get_history()) == 2

print("PASS: Failed exchange did not modify memory.")

# Simulate another successful response.
with patch(
    "Agent.llm.generate_with_fallback",
    return_value="Factorial is a classic recursive example."
) as mock_router:

    ask_llm("Give me an example.", memory)

    sent_contents = mock_router.call_args.args[1]

    assert len(sent_contents) == 3
    assert sent_contents[0].role == "user"
    assert sent_contents[1].role == "model"
    assert sent_contents[2].role == "user"

assert len(memory.get_history()) == 4

print("PASS: Previous context supplied to model.")
print("PASS: Conversation history updated correctly.")

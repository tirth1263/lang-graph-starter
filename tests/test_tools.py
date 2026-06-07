from tools import count_words_in_text, current_time_for_timezone


def test_count_words_in_text_counts_words_and_contractions():
    assert count_words_in_text("The quick brown fox jumps.") == 5
    assert count_words_in_text("LangGraph's ReAct loop works.") == 4


def test_current_time_for_unknown_timezone_returns_helpful_message():
    message = current_time_for_timezone("Moon/Base")

    assert "Unknown timezone" in message
    assert "IANA timezone" in message

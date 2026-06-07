from __future__ import annotations

import re
from datetime import datetime
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from langchain_core.tools import tool


def count_words_in_text(text: str) -> int:
    """Count words in a string using simple word boundaries."""
    return len(re.findall(r"\b[\w'-]+\b", text))


def current_time_for_timezone(timezone_name: str = "UTC") -> str:
    """Format the current time for an IANA timezone."""
    try:
        timezone = ZoneInfo(timezone_name)
    except ZoneInfoNotFoundError:
        return (
            f"Unknown timezone '{timezone_name}'. "
            "Use an IANA timezone such as 'UTC', 'America/New_York', or 'Asia/Kolkata'."
        )

    return datetime.now(timezone).strftime("%Y-%m-%d %H:%M:%S %Z%z")


@tool
def get_current_time(timezone_name: str = "UTC") -> str:
    """Return the current date and time for an IANA timezone name."""
    return current_time_for_timezone(timezone_name)


@tool
def word_count(text: str) -> str:
    """Count the words in the provided text."""
    count = count_words_in_text(text)
    return f"{count} word{'s' if count != 1 else ''}"

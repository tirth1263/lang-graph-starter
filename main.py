from __future__ import annotations

import os
from typing import Any

from dotenv import load_dotenv
from langchain_core.messages import AIMessage, HumanMessage
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent

from tools import get_current_time, word_count


SYSTEM_PROMPT = """
You are a concise, helpful LangGraph ReAct assistant.
Use get_current_time whenever the user asks about the current time.
Use word_count whenever the user asks how many words are in some text.
For general questions, answer directly and keep the response practical.
"""


def build_agent():
    """Create the prebuilt LangGraph ReAct agent."""
    load_dotenv()

    api_key = os.getenv("NEBIUS_API_KEY")
    if not api_key:
        raise RuntimeError(
            "NEBIUS_API_KEY is not set. Copy .env.example to .env and add your key."
        )

    model = ChatOpenAI(
        model=os.getenv("NEBIUS_MODEL", "Qwen/Qwen3-30B-A3B"),
        api_key=api_key,
        base_url=os.getenv("NEBIUS_BASE_URL", "https://api.tokenfactory.nebius.com/v1/"),
        temperature=float(os.getenv("NEBIUS_TEMPERATURE", "0")),
    )

    return create_react_agent(
        model=model,
        tools=[get_current_time, word_count],
        prompt=SYSTEM_PROMPT,
    )


def stringify_content(content: Any) -> str:
    """Normalize message content from OpenAI-compatible responses."""
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts: list[str] = []
        for item in content:
            if isinstance(item, dict) and "text" in item:
                parts.append(str(item["text"]))
            else:
                parts.append(str(item))
        return "\n".join(parts)
    return str(content)


def latest_ai_message(messages: list[Any]) -> str:
    """Return the most recent non-empty AI response in the graph state."""
    for message in reversed(messages):
        if isinstance(message, AIMessage) and message.content:
            return stringify_content(message.content)
    return "No assistant response was returned."


def main() -> None:
    agent = build_agent()
    messages: list[Any] = []

    print("LangGraph Starter")
    print("Ask a question, or type 'exit' to quit.\n")

    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in {"exit", "quit", "q"}:
            print("Goodbye!")
            break
        if not user_input:
            continue

        messages.append(HumanMessage(content=user_input))
        result = agent.invoke({"messages": messages})
        messages = result["messages"]

        print(f"\nAssistant: {latest_ai_message(messages)}\n")


if __name__ == "__main__":
    main()

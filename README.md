# LangGraph Starter

A minimal, production-minded starter for building stateful graph-based LLM applications with LangGraph. The project uses the prebuilt `create_react_agent` helper to assemble a ReAct loop that can reason, call tools, observe results, and continue the conversation with message state.

This starter is powered by Nebius Token Factory through `ChatOpenAI`, using Nebius' OpenAI-compatible API endpoint and the `Qwen/Qwen3-30B-A3B` model.

## Why This Project Exists

LangGraph is excellent when you want an agent that can do more than answer once and disappear. This starter keeps the moving parts intentionally small so you can see the core idea clearly:

1. User sends a message.
2. The graph decides whether it should answer directly or call a tool.
3. A Python tool runs and returns an observation.
4. The model uses that observation to produce the final response.
5. The conversation history stays in the graph's `messages` state.

The result is a clean foundation for agentic apps, tool-using assistants, workflow automations, research bots, or any LLM system that needs memory across turns.

## Features

- Prebuilt ReAct agent from `langgraph.prebuilt.create_react_agent`
- Nebius Token Factory integration through `langchain-openai`
- OpenAI-compatible `ChatOpenAI` configuration with a custom `base_url`
- Two auto-callable Python tools:
  - `get_current_time`
  - `word_count`
- Multi-turn CLI conversation using LangGraph message state
- Environment-based configuration through `.env`
- Focused tests for the local tool logic
- Static project website included in `docs/`

## Project Structure

```text
.
├── main.py                 # CLI app and LangGraph agent setup
├── tools.py                # @tool-decorated Python tools
├── tests/
│   └── test_tools.py       # Tool unit tests
├── docs/
│   └── index.html          # Published project website
├── .env.example            # Nebius configuration template
├── requirements.txt        # Runtime dependencies
├── requirements-dev.txt    # Test dependencies
└── README.md
```

## Prerequisites

- Python 3.10+
- A Nebius API key from [Nebius Token Factory](https://studio.nebius.ai/)

## Installation

```bash
git clone https://github.com/tirth1263/lang-graph-starter.git
cd lang-graph-starter

python -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
```

On Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1

pip install -r requirements.txt
```

Create your local environment file:

```bash
cp .env.example .env
```

Then set your Nebius key:

```env
NEBIUS_API_KEY=your_nebius_api_key_here
NEBIUS_BASE_URL=https://api.tokenfactory.nebius.com/v1/
NEBIUS_MODEL=Qwen/Qwen3-30B-A3B
NEBIUS_TEMPERATURE=0
```

## Usage

```bash
python main.py
```

Example queries:

- `What time is it right now in America/Phoenix?`
- `How many words are in 'the quick brown fox jumps'?`
- `Explain the ReAct pattern in two sentences.`

## How It Works

The app creates a `ChatOpenAI` model pointed at the Nebius Token Factory OpenAI-compatible endpoint:

```python
model = ChatOpenAI(
    model="Qwen/Qwen3-30B-A3B",
    api_key=os.getenv("NEBIUS_API_KEY"),
    base_url="https://api.tokenfactory.nebius.com/v1/",
)
```

That model is passed into LangGraph's prebuilt ReAct agent with two Python tools:

```python
agent = create_react_agent(
    model=model,
    tools=[get_current_time, word_count],
)
```

When a user asks for the current time or asks for a word count, the model can call the matching tool automatically. Otherwise, it can answer directly.

## Run Tests

```bash
pip install -r requirements-dev.txt
pytest
```

## Deployment

The static website lives in `docs/` and is ready for GitHub Pages or any static host.

GitHub Pages setup:

1. Open the repository settings on GitHub.
2. Go to **Pages**.
3. Select **Deploy from a branch**.
4. Choose the `main` branch and the `/docs` folder.

## Ideas To Extend It

- Add more domain tools such as web search, database lookup, or file analysis.
- Replace the CLI with a FastAPI backend.
- Add checkpointers for persisted memory.
- Stream model responses to the terminal or browser.
- Add a human approval step before sensitive tool calls.

## References

- [LangGraph](https://github.com/langchain-ai/langgraph)
- [LangChain OpenAI Integration](https://python.langchain.com/docs/integrations/chat/openai/)
- [Nebius Token Factory Documentation](https://docs.tokenfactory.nebius.com/api-reference/introduction)

## License

MIT

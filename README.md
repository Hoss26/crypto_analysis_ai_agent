# Crypto Analysis Agent

An AI agent that answers questions about cryptocurrencies, live market data and recent news. It is built with **LangGraph** and follows the **ReAct** (Reason + Act) architecture.

## Table of Contents

- [Architecture: ReAct](#architecture-react)
- [Features](#features)
- [Tools](#tools)
- [API Keys](#api-keys)
- [Setup](#setup)
- [Usage](#usage)
- [Notes](#notes)

## Architecture: ReAct

The agent runs in a loop of reasoning and acting:

1. **Reason**: the LLM reads the conversation and decides what to do next.
2. **Act**: if it needs data, it calls one of its tools.
3. **Observe**: the tool result is added to the conversation.
4. **Repeat** until the LLM has enough information, then it writes the final answer.

```text
User question
     |
     v
 +-----------+   tool call    +-----------+
 | Assistant | -------------> |   Tools   |
 |   (LLM)   | <------------- | (APIs)    |
 +-----------+  tool result   +-----------+
     |
     v
Final answer
```

In LangGraph, this is a graph with an `assistant` node (the LLM with a system prompt) and a `tools` node, connected by a conditional edge that routes to the tools whenever the model requests one.

## Features

- ReAct agent built with LangGraph
- Custom system prompt defining the agent's personality and rules (a professional crypto market analyst that never invents prices or metrics)
- Conversation memory using `MemorySaver` and a `thread_id`, so follow-up questions work
- Interactive chat loop

## Tools

| Tool | Description | Data source |
|------|-------------|-------------|
| `crypto_list_tool(limit)` | Condensed list of available crypto tickers | FreeCryptoAPI |
| `crypto_data_tool(symbol)` | Market data for a ticker such as BTC or ETH | FreeCryptoAPI |
| `crypto_news_tool(query, max_items)` | Recent headlines, sources and URLs | NewsAPI |

## API Keys

This project uses **3 API keys**:

| Key | Service | Used for |
|-----|---------|----------|
| `GROQ_API_KEY` | [Groq](https://console.groq.com) | The LLM that powers the agent |
| `FREECRYPTO_TOKEN` | [FreeCryptoAPI](https://freecryptoapi.com) | Crypto market data |
| `NEWS_API_KEY` | [NewsAPI](https://newsapi.org) | Crypto news |

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_key
FREECRYPTO_TOKEN=your_freecryptoapi_token
NEWS_API_KEY=your_newsapi_key
```

> Never commit this file. Make sure `.env` is listed in `.gitignore`.

## Setup

```bash
git clone https://github.com/Hoss26/crypto_analysis_ai_agent.git
cd crypto_analysis_ai_agent

python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

pip install langgraph langchain-core langchain-groq newsapi-python requests python-dotenv
```

## Usage

1. Open `notebooks/project.ipynb` in VS Code or Jupyter.
2. Select the `.venv` kernel.
3. Run the cells in order: imports and keys, tools, system prompt, model, graph, then the chat loop.

Example questions:

- "What is the current price of BTC?"
- "Compare BTC and ETH. Which looks stronger?"
- "Summarize the latest Ethereum news in 3 bullets."

Follow-up questions such as "Which one did you say was stronger?" work as long as you reuse the same `thread_id`:

```python
config = {"configurable": {"thread_id": "1"}}
```

## Notes

- Free API tiers have rate limits. If you see a 429 error from Groq, lower `max_tokens` or wait a minute.
- `MemorySaver` keeps history in RAM only, so it is cleared when the kernel restarts.

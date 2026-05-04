# Valura AI — Team Lead Project Assignment

AI agent ecosystem that helps a novice investor build, monitor, grow, and protect a portfolio.

## What this implements
- Multi-agent orchestration for:
  - Planning (`PlannerAgent`)
  - Monitoring (`MonitorAgent`)
  - Risk guardrails (`GuardrailAgent`)
  - Rebalancing actions (`RebalanceAgent`)
- SSE streaming output (`POST /advice/stream`) with stage-by-stage events.
- API-first workflow to store investor profile + portfolio.
- Mock-first LLM integration so tests pass without an API key.

## Tech Stack
- Python + FastAPI
- SSE via `sse-starlette`
- Pydantic / pydantic-settings
- `httpx` for OpenAI Responses API integration
- `pytest` + `pytest-asyncio`

## Persistence choice
I chose **in-memory persistence** for this submission.

Why:
1. Zero external infra and fastest evaluator setup.
2. Deterministic behavior for tests.
3. Keeps focus on agent architecture and streaming protocol.

Tradeoff:
- Data is volatile (resets on process restart).

## Project Structure
- `src/main.py` — app factory + endpoints
- `src/service.py` — orchestration service
- `src/agents.py` — specialized investing agents
- `src/models.py` — request/response and domain models
- `src/repository.py` — in-memory persistence
- `src/llm.py` — mock + OpenAI-backed client
- `src/config.py` — env configuration
- `tests/` — API and service tests

## Setup
```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
# venv\Scripts\activate  # Windows
pip install -r requirements.txt
cp .env.example .env
```

## Required environment variables
- `USE_MOCK_LLM` (`true`/`false`) — **required for predictable mode selection**.
- `MODEL` — model name used when `USE_MOCK_LLM=false`.

## Optional environment variables
- `OPENAI_API_KEY` — required only when `USE_MOCK_LLM=false`.
- `DATABASE_URL` — reserved for future persistent storage backend.

## Run
```bash
uvicorn src.main:app --reload
```

## API Endpoints
- `GET /health`
- `POST /profiles`
- `POST /portfolios`
- `POST /advice/stream` (SSE)

### SSE demo
```bash
curl -N -X POST http://127.0.0.1:8000/advice/stream \
  -H "Content-Type: application/json" \
  -d '{"user_id":"u1","question":"How should I improve my portfolio?"}'
```

## Test
```bash
pytest tests/ -v
```

## Non-obvious decisions
1. Added an app factory (`create_app`) to keep startup dependency wiring explicit and test-friendly.
2. Kept LLM integration behind a lightweight protocol (`LLMClient`) for easy mocking/substitution.
3. Streaming emits named SSE events (`planner`, `monitor`, `guardrail`, `rebalancer`, `advisor`, `done`) so clients can render workflow progress in real time.

## Defence video (≤10 min)
- https://example.com/valura-defence-video

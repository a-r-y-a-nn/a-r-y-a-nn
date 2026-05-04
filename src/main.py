from __future__ import annotations

import asyncio
import json

from fastapi import FastAPI, HTTPException
from sse_starlette.sse import EventSourceResponse

from .config import settings
from .llm import MockLLM, OpenAIResponsesLLM
from .models import AdviceRequest, InvestorProfile, Portfolio
from .repository import InMemoryRepository
from .service import OrchestratorService


def create_app() -> FastAPI:
    app = FastAPI(title="Valura AI Investor Agent")
    repo = InMemoryRepository()

    if settings.use_mock_llm or not settings.openai_api_key:
        llm = MockLLM()
    else:
        llm = OpenAIResponsesLLM(api_key=settings.openai_api_key, model=settings.model)

    service = OrchestratorService(repo=repo, llm=llm)

    @app.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok"}

    @app.post("/profiles")
    def create_profile(profile: InvestorProfile) -> dict[str, str]:
        repo.save_profile(profile)
        return {"status": "saved", "user_id": profile.user_id}

    @app.post("/portfolios")
    def create_portfolio(portfolio: Portfolio) -> dict[str, str]:
        if not repo.get_profile(portfolio.user_id):
            raise HTTPException(status_code=404, detail="Profile not found")
        repo.save_portfolio(portfolio)
        return {"status": "saved", "user_id": portfolio.user_id}

    @app.post("/advice/stream")
    async def stream_advice(request: AdviceRequest) -> EventSourceResponse:
        async def event_generator():
            messages = await service.build_messages(request)
            for msg in messages:
                yield {"event": msg.agent, "data": json.dumps(msg.model_dump())}
                await asyncio.sleep(0)
            yield {"event": "done", "data": "[DONE]"}

        return EventSourceResponse(event_generator())

    return app


app = create_app()

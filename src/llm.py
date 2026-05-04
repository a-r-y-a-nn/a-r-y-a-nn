from __future__ import annotations

from typing import Protocol

import httpx


class LLMClient(Protocol):
    async def complete(self, prompt: str) -> str: ...


class MockLLM:
    async def complete(self, prompt: str) -> str:
        return f"MOCK_RESPONSE: {prompt[:120]}"


class OpenAIResponsesLLM:
    def __init__(self, api_key: str, model: str):
        self.api_key = api_key
        self.model = model

    async def complete(self, prompt: str) -> str:
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.post(
                "https://api.openai.com/v1/responses",
                headers={"Authorization": f"Bearer {self.api_key}"},
                json={"model": self.model, "input": prompt},
            )
            response.raise_for_status()
            data = response.json()
        return data.get("output_text", "") or "No response generated."

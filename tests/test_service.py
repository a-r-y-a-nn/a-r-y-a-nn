import pytest

from src.llm import MockLLM
from src.models import AdviceRequest, InvestorProfile, Portfolio
from src.repository import InMemoryRepository
from src.service import OrchestratorService


@pytest.mark.asyncio
async def test_service_returns_setup_prompt_when_missing_data():
    repo = InMemoryRepository()
    service = OrchestratorService(repo=repo, llm=MockLLM())

    messages = await service.build_messages(AdviceRequest(user_id="missing", question="help"))

    assert len(messages) == 1
    assert messages[0].agent == "system"


@pytest.mark.asyncio
async def test_service_returns_advisor_message():
    repo = InMemoryRepository()
    repo.save_profile(
        InvestorProfile(
            user_id="u1",
            age=28,
            monthly_income=8000,
            emergency_fund_months=6,
            risk_tolerance="medium",
            investment_horizon_years=10,
        )
    )
    repo.save_portfolio(Portfolio(user_id="u1", cash=1000, holdings=[]))
    service = OrchestratorService(repo=repo, llm=MockLLM())

    messages = await service.build_messages(AdviceRequest(user_id="u1", question="What next?"))

    assert messages[-1].agent == "advisor"
    assert messages[-1].content.startswith("MOCK_RESPONSE")

from __future__ import annotations

from .agents import GuardrailAgent, MonitorAgent, PlannerAgent, RebalanceAgent
from .llm import LLMClient
from .models import AdviceRequest, AgentMessage
from .repository import InMemoryRepository


class OrchestratorService:
    def __init__(self, repo: InMemoryRepository, llm: LLMClient):
        self.repo = repo
        self.llm = llm
        self.planner = PlannerAgent()
        self.monitor = MonitorAgent()
        self.guardrail = GuardrailAgent()
        self.rebalance = RebalanceAgent()

    async def build_messages(self, req: AdviceRequest) -> list[AgentMessage]:
        profile = self.repo.get_profile(req.user_id)
        portfolio = self.repo.get_portfolio(req.user_id)
        if not profile or not portfolio:
            return [AgentMessage(agent="system", content="Please create profile and portfolio first.")]

        messages = [
            AgentMessage(agent="planner", content=self.planner.run(profile)),
            AgentMessage(agent="monitor", content=self.monitor.run(portfolio)),
            AgentMessage(agent="guardrail", content=self.guardrail.run(profile, portfolio)),
        ]
        actions = self.rebalance.run(profile, portfolio)
        messages.append(
            AgentMessage(
                agent="rebalancer",
                content="; ".join([f"{a.action.upper()} {a.symbol}: {a.reason}" for a in actions]),
            )
        )
        synthesis_prompt = "\n".join([m.content for m in messages] + [f"User question: {req.question}"])
        final = await self.llm.complete(synthesis_prompt)
        messages.append(AgentMessage(agent="advisor", content=final))
        return messages

from __future__ import annotations

from .models import InvestorProfile, Portfolio, RebalanceAction


class PlannerAgent:
    def run(self, profile: InvestorProfile) -> str:
        risk_map = {
            "low": "capital preservation and broad diversification",
            "medium": "balanced growth with diversified ETFs",
            "high": "growth focus with higher equity allocation",
        }
        return (
            f"Plan for {profile.user_id}: prioritize {risk_map[profile.risk_tolerance]}; "
            f"target horizon {profile.investment_horizon_years} years."
        )


class MonitorAgent:
    def run(self, portfolio: Portfolio) -> str:
        concentration = "none"
        if portfolio.holdings:
            max_qty = max(portfolio.holdings, key=lambda h: h.quantity)
            concentration = max_qty.symbol
        return f"Monitoring: cash={portfolio.cash:.2f}, largest position={concentration}."


class GuardrailAgent:
    def run(self, profile: InvestorProfile, portfolio: Portfolio) -> str:
        warnings: list[str] = []
        if profile.emergency_fund_months < 3:
            warnings.append("Emergency fund below 3 months")
        if len(portfolio.holdings) > 10 and profile.risk_tolerance == "low":
            warnings.append("Portfolio complexity may exceed conservative profile")
        return "; ".join(warnings) if warnings else "No critical guardrail issues."


class RebalanceAgent:
    def run(self, profile: InvestorProfile, portfolio: Portfolio) -> list[RebalanceAction]:
        actions: list[RebalanceAction] = []
        if not portfolio.holdings:
            actions.append(
                RebalanceAction(symbol="VTI", action="buy", reason="Start diversified core index exposure")
            )
            return actions
        for holding in portfolio.holdings:
            actions.append(RebalanceAction(symbol=holding.symbol, action="hold", reason="No drift signal in mock logic"))
        return actions

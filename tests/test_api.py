from fastapi.testclient import TestClient

from src.main import create_app


client = TestClient(create_app())


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_portfolio_requires_profile():
    portfolio_payload = {"user_id": "u404", "cash": 1000, "holdings": []}
    response = client.post("/portfolios", json=portfolio_payload)
    assert response.status_code == 404


def test_end_to_end_streaming():
    profile_payload = {
        "user_id": "u1",
        "age": 30,
        "monthly_income": 7000,
        "emergency_fund_months": 2,
        "risk_tolerance": "medium",
        "investment_horizon_years": 15,
    }
    assert client.post("/profiles", json=profile_payload).status_code == 200

    portfolio_payload = {
        "user_id": "u1",
        "cash": 1200,
        "holdings": [{"symbol": "AAPL", "quantity": 2, "average_cost": 150}],
    }
    assert client.post("/portfolios", json=portfolio_payload).status_code == 200

    with client.stream("POST", "/advice/stream", json={"user_id": "u1", "question": "What should I do next?"}) as r:
        body = "".join([chunk.decode() if isinstance(chunk, bytes) else chunk for chunk in r.iter_text()])
        assert r.status_code == 200
        assert "event: planner" in body
        assert "event: advisor" in body
        assert "event: done" in body

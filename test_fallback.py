from app.services.fallback import (
    home_fallback,
    jewelry_fallback,
    party_fallback,
)


def test_home_budget():
    result = home_fallback(
        budget=100000,
        rooms=["Living Room", "Bedroom"],
        style="Modern",
    )

    assert result["total_estimated"] <= 100000
    assert result["remaining_budget"] >= 0
    assert result["planner_type"] == "home"


def test_party_budget():
    result = party_fallback(
        budget=50000,
        guests=50,
        event_type="Birthday",
    )

    assert result["total_estimated"] <= 50000
    assert result["remaining_budget"] >= 0
    assert result["planner_type"] == "party"


def test_jewelry_budget():
    result = jewelry_fallback(
        budget=30000,
        occasion="Wedding",
        outfit_description="Red traditional dress",
    )

    assert result["total_estimated"] <= 30000
    assert result["remaining_budget"] >= 0
    assert result["planner_type"] == "jewelry"
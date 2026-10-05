import os
import tempfile

os.environ["DATABASE_URL"] = (
    "sqlite:///" +
    os.path.join(
        tempfile.gettempdir(),
        "pocketsmart_test.db",
    )
)

from fastapi.testclient import TestClient

from app.database import Base, engine
from app.main import app


Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)


client = TestClient(app)


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_home_page():
    response = client.get("/")

    assert response.status_code == 200
    assert "PocketSmart AI" in response.text


def test_register():
    response = client.post(
        "/register",
        data={
            "username": "testuser",
            "email": "test@example.com",
            "password": "password123",
        },
        follow_redirects=False,
    )

    assert response.status_code == 303
    assert "/login" in response.headers["location"]


def test_login():
    response = client.post(
        "/login",
        data={
            "username": "testuser",
            "password": "password123",
        },
        follow_redirects=False,
    )

    assert response.status_code == 303
    assert "access_token" in response.cookies


def test_home_planner():
    login = client.post(
        "/login",
        data={
            "username": "testuser",
            "password": "password123",
        },
        follow_redirects=False,
    )

    cookies = login.cookies

    response = client.post(
        "/generate-home",
        data=[
            ("budget", "100000"),
            ("rooms", "Living Room"),
            ("rooms", "Bedroom"),
            ("style", "Modern"),
            ("notes", "Simple design"),
        ],
        cookies=cookies,
        follow_redirects=False,
    )

    assert response.status_code == 303
    assert "/recommendations/" in response.headers["location"]


def test_dashboard_requires_login():
    fresh_client = TestClient(app)

    response = fresh_client.get(
        "/dashboard",
        follow_redirects=False,
    )

    assert response.status_code == 303
    assert response.headers["location"] == "/login"
import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_login_success():
    response = client.post(
        "/auth/token",
        json={"username": "admin", "password": "admin123"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert data["expires_in"] == 300


def test_login_wrong_password():
    response = client.post(
        "/auth/token",
        json={"username": "admin", "password": "wrongpassword"},
    )
    assert response.status_code == 401


def test_login_wrong_username():
    response = client.post(
        "/auth/token",
        json={"username": "unknown", "password": "admin123"},
    )
    assert response.status_code == 401


def test_refresh_token_success():
    login_response = client.post(
        "/auth/token",
        json={"username": "admin", "password": "admin123"},
    )
    token = login_response.json()["access_token"]

    refresh_response = client.post(
        "/auth/refresh",
        headers={"Authorization": "Bearer " + token},
    )
    assert refresh_response.status_code == 200
    data = refresh_response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert data["expires_in"] == 300


def test_refresh_token_invalid():
    response = client.post(
        "/auth/refresh",
        headers={"Authorization": "Bearer notavalidtoken"},
    )
    assert response.status_code == 401

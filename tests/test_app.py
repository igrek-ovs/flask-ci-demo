import pytest

import app as app_module


@pytest.fixture
def client():
    app_module.app.config.update(TESTING=True)
    return app_module.app.test_client()


def test_index(client):
    response = client.get("/")
    assert response.status_code == 200
    data = response.get_json()
    assert data["message"] == "Hello"
    assert "host" in data


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}


def test_count_without_database(client, monkeypatch):
    monkeypatch.setattr(app_module, "DATABASE_URL", None)
    response = client.get("/count")
    assert response.status_code == 503

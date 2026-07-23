"""Tests for app.py: the task count API endpoint."""
import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import app as app_module


@pytest.fixture
def client():
    app_module.app.config["TESTING"] = True
    app_module._tasks.clear()
    with app_module.app.test_client() as client:
        client.post("/login", data={"username": "alice", "password": "wonderland"})
        yield client
    app_module._tasks.clear()


def test_task_count_starts_at_zero(client):
    response = client.get("/api/tasks/count")
    assert response.status_code == 200
    assert response.get_json() == {"count": 0}


def test_task_count_after_adding_a_task(client):
    client.post("/tasks/add", data={"title": "Buy milk"})
    response = client.get("/api/tasks/count")
    assert response.status_code == 200
    assert response.get_json() == {"count": 1}


def test_task_count_requires_login():
    app_module.app.config["TESTING"] = True
    with app_module.app.test_client() as client:
        response = client.get("/api/tasks/count")
        assert response.status_code == 302


def test_health_check():
    app_module.app.config["TESTING"] = True
    with app_module.app.test_client() as client:
        response = client.get("/health")
        assert response.status_code == 200
        assert response.get_json() == {"status": "ok"}

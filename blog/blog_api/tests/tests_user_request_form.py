import pytest
from rest_framework.test import APIClient


URL = "/api/user_demo_request/"


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def valid_payload():
    return {
        "name": "John",
        "email": "john@example.com",
        "motive_text": "I want to see a demo of your product.",
    }


def test_user_demo_request_success(client, valid_payload):
    response = client.post(URL, valid_payload, format="json")
    assert response.status_code == 201
    assert "message" in response.data
    assert "John" in response.data["message"]


@pytest.mark.parametrize("name", ["valera", "Valera", "VALERA", "Super Valera"])
def test_user_demo_request_valera_name_rejected(client, valid_payload, name):
    valid_payload["name"] = name
    response = client.post(URL, valid_payload, format="json")
    assert response.status_code == 400
    assert "name" in response.data


def test_user_demo_request_empty_body(client):
    response = client.post(URL, {}, format="json")
    assert response.status_code == 400
    assert "name" in response.data
    assert "email" in response.data
    assert "motive_text" in response.data

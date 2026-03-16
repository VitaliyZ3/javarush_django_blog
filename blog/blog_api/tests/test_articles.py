import pytest
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.models import User, Group

CREATE_URL = "/api/articles/"

@pytest.fixture
def test_moderator_user(db):
    group = Group.objects.create(name="Moderator")
    user = User.objects.create_user(username="root", password="root")
    user.groups.set([group])
    return user

@pytest.fixture
def test_user(db):
    return User.objects.create_user(username="root", password="root")

@pytest.fixture
def client():
    return APIClient()

@pytest.fixture
def valid_payload():
    return {
      "name": "Test Article",
      "text": "Test Article Text"
    }

def test_article_create_unauthorized(client, valid_payload):
    response = client.post(CREATE_URL, valid_payload, format="json")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

def test_article_create_moderator_success(client, valid_payload, test_moderator_user):
    client.force_authenticate(test_moderator_user)
    response = client.post(CREATE_URL, valid_payload, format="json")
    assert response.status_code == status.HTTP_201_CREATED

def test_article_create_user_failed(client, valid_payload, test_user):
    client.force_authenticate(test_user)
    response = client.post(CREATE_URL, valid_payload, format="json")
    assert response.status_code == status.HTTP_403_FORBIDDEN

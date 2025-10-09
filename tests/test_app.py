import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)

def test_signup_for_activity():
    # Use a test activity and email
    activity = list(client.get("/activities").json().keys())[0]
    email = "testuser@example.com"
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 200 or response.status_code == 400
    # Try duplicate signup
    response_dup = client.post(f"/activities/{activity}/signup?email={email}")
    assert response_dup.status_code == 400
    assert "already signed up" in response_dup.json().get("detail", "")

def test_unregister_participant():
    activity = list(client.get("/activities").json().keys())[0]
    email = "testuser@example.com"
    # Unregister participant
    response = client.post(f"/activities/{activity}/unregister?email={email}")
    assert response.status_code == 200 or response.status_code == 400
    # Try to unregister again (should fail)
    response_dup = client.post(f"/activities/{activity}/unregister?email={email}")
    assert response_dup.status_code == 400
    assert "not registered" in response_dup.json().get("detail", "")

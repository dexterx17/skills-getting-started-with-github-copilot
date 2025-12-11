import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data

def test_signup_and_unregister():
    activity = "Chess Club"
    email = "testuser@mergington.edu"
    # Signup
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 200
    assert email in response.json()["message"]
    # Duplicate signup should fail
    response_dup = client.post(f"/activities/{activity}/signup?email={email}")
    assert response_dup.status_code == 400
    # Unregister
    response_del = client.delete(f"/activities/{activity}/unregister?email={email}")
    assert response_del.status_code == 200
    assert email in response_del.json()["message"]
    # Unregister again should fail
    response_del2 = client.delete(f"/activities/{activity}/unregister?email={email}")
    assert response_del2.status_code == 404

def test_signup_invalid_activity():
    response = client.post("/activities/Nonexistent/signup?email=foo@bar.com")
    assert response.status_code == 404

def test_unregister_invalid_activity():
    response = client.delete("/activities/Nonexistent/unregister?email=foo@bar.com")
    assert response.status_code == 404

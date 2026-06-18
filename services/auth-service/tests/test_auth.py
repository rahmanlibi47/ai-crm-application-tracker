import uuid
from fastapi.testclient import TestClient
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))
from app.main import app

client = TestClient(app)

# def test_health_check():
#     response = client.get("/health")
    
#     assert response.status_code == 200
#     assert response.json() == {
#         "status": "auth service running"
#     }
def test_signup():

    email = f"{uuid.uuid4()}@test.com"

    response = client.post(
        "/signup",
        json={
            "email": email,
            "password": "Password123",
            "full_name": "Test User"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data
    assert data["token_type"] == "bearer"

    assert data["user"]["email"] == email
    assert data["user"]["full_name"] == "Test User"


def test_login():

    email = f"{uuid.uuid4()}@test.com"

    signup_response = client.post(
        "/signup",
        json={
            "email": email,
            "password": "Password123",
            "full_name": "Login User"
        }
    )

    assert signup_response.status_code == 200

    response = client.post(
        "/login",
        json={
            "email": email,
            "password": "Password123"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data
    assert data["token_type"] == "bearer"

    assert data["user"]["email"] == email
    
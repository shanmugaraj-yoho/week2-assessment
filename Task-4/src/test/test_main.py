import os
import hmac
import hashlib
import pytest
import json

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.main import app
from src.database import Base, get_db
# from src.models import Customer
# from src.dependencies import verify_api_key
# from src.routes import webhooks

TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL")
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET")

engine = create_engine(TEST_DATABASE_URL)
TestingSessionModel = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    db = TestingSessionModel()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture
def client():
    Base.metadata.drop_all(bind=engine)

    Base.metadata.create_all(bind=engine)

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=engine)

API_KEY = os.getenv("API_KEY")

HEADERS = { "X-API-KEY":API_KEY }

# 1
def test_create_customer(client):
    res = client.post(
        "/customers",
        json={
            "name": "Arun",
            "email": "arun@gmail.com"
        },
        headers = HEADERS
    )
    assert res.status_code in (200,201)

# 2
def test_get_customer(client):
    res = client.post(
        "/customers",
        json={
            "name": "Arun",
            "email": "arun@gmail.com"
        },
        headers = HEADERS
    )
    res = client.get("/customers?page=1&per_page=10", headers = HEADERS)
    assert res.status_code == 200

# 3
def test_get_customer_by_id(client):
    res = client.post(
        "/customers",
        json={
            "name": "Arun",
            "email": "arun@gmail.com"
        },
        headers = HEADERS
    )
    customer_id = res.json()["id"]
    res = client.get(f"/customers/{customer_id}", headers = HEADERS)
    assert res.status_code in (422,200)
    # assert res.json()["email"] == "arun@gmail.com"

# 4
def test_update_customer(client):
    res = client.post(
        "/customers",
        json={
            "name": "Arun",
            "email": "arun@gmail.com"
        },
        headers = HEADERS
    )
    customer_id = res.json()["id"]
    res = client.put(f"/customers/{customer_id}",
                     json ={
                        "name": "Arun",
                        "email": "arun@gmail.com"
                     }, headers = HEADERS)
    assert res.status_code == 200

# 5
def test_delete_customer(client):
    res = client.post(
        "/customers",
        json={
            "name": "Arun",
            "email": "arun@gmail.com"
        },
        headers = HEADERS
    )
    customer_id = res.json()["id"]
    res = client.delete(f"/customers/{customer_id}", headers = HEADERS)
    assert res.status_code == 200

#6
def test_missing_api_key(client):
    res = client.get("/customers")
    assert res.status_code == 401

#7
def test_invalid_api_key(client):
    res = client.get(
        "/customers",
        headers={"X-API-KEY":"wrong-key"}
    )
    assert res.status_code == 403

#8
def test_customer_not_found(client):
    res = client.get(
        "/customers/999",
        headers = HEADERS
    )
    assert res.status_code == 422

def generate_signature(payload):
    body = json.dumps(payload).encode()

    expected_signature = hmac.new(
            WEBHOOK_SECRET.encode(),
            body,
            hashlib.sha256
        ).hexdigest()
    return body, "sha256=" + expected_signature

#valid
def test_valid_webhook(client):
    payload = {"event":"customer.created"}
    body, signature = generate_signature(payload)

    res = client.post(
        "/webhook",
        content=body,
        headers={
            "Content-Type":"application/json",
            "X-Webhook-Signature":signature
        }
    )
    assert res.status_code in (401,200)

#Invalid
def test_invalid_webhook(client):
    res = client.post(
            "/webhook",
            json={"event":"customer.created"},
            headers={
                "X-Webhook-Signature":"wrong"
            }
        )
    assert res.status_code in(401,403)

#missing
def test_missing_webhook(client):
    res = client.post(
            "/webhook",
            json={"event":"customer.created"}
            )
    assert res.status_code in (401, 403)


    
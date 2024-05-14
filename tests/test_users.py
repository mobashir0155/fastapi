# from fastapi.testclient import TestClient
# from app.main import app
import pytest
from app import schemas
from jose import jwt
from app.config import configs

# client = TestClient(app)

def test_root(client):
    res = client.get("/")
    assert res.json().get("message") == "Hello World"

def test_create_user(client):
    res = client.post("/users/", json={"email": "user2@gmail.com", "password": "12345678"})
    new_user = schemas.User(**res.json())
    assert new_user.email == "user2@gmail.com"
    assert res.status_code == 201

def test_login_user(client, test_user):
    res = client.post("/login", data={"username": test_user['email'], "password": test_user['password']})
    res_user = schemas.Token(**res.json())
    payload = jwt.decode(res_user.access_token, configs.jwt_secret, algorithms=[configs.jwt_algorithm])
    user_id: str = payload.get("user_id")

    assert test_user["id"] == user_id
    assert res.status_code == 200

@pytest.mark.parametrize("email,password,status_code",[
    ("wrongemail@test.com", "password", 403),
    ("user2@gmail.com", "123456789", 403),
    (None, "123456789", 422)
])
def test_invalid_user(client,email,password,status_code):
    res = client.post("/login", data={"username": email, "password": password})

    assert res.status_code == status_code
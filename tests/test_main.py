from fastapi.testclient import TestClient

# Тест 1: Реєстрація користувача
def test_register_user(client: TestClient):
    response = client.post(
        "/users/register",
        json={"email": "testuser@example.com", "password": "strongpassword123"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "testuser@example.com"
    assert "id" in data

# Тест 2: Успішний логін та отримання токена
def test_login_user(client: TestClient):
    client.post(
        "/users/register",
        json={"email": "loginuser@example.com", "password": "password123"}
    )
    response = client.post(
        "/users/login",
        data={"username": "loginuser@example.com", "password": "password123"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

# Тест 3: Створення події (Захищений маршрут)
def test_create_event(client: TestClient):
    # 1. Реєструємо та логінимо юзера
    client.post(
        "/users/register",
        json={"email": "owner@example.com", "password": "password123"}
    )
    login_resp = client.post(
        "/users/login",
        data={"username": "owner@example.com", "password": "password123"}
    )
    token = login_resp.json()["access_token"]

    # 2. Робимо запит на створення події з Bearer токеном
    headers = {"Authorization": f"Bearer {token}"}
    event_data = {
        "title": "Тестова подія Pytest",
        "description": "Перевірка працездатності юніт-тестов",
        "date": "2026-07-20T18:00:00",
        "location": "Тестова локація"
    }
    
    response = client.post("/events/", json=event_data, headers=headers) 
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Тестова подія Pytest" 
    assert "id" in data
    assert "owner_id" in data
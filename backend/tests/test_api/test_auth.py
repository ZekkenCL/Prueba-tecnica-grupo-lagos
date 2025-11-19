"""
Tests para API de autenticación
"""
import pytest


@pytest.mark.integration
def test_register_new_user(client):
    """Test de registro de nuevo usuario"""
    response = client.post(
        "/api/auth/register",
        json={
            "email": "newuser@example.com",
            "username": "newuser",
            "password": "securepass123"
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "newuser@example.com"
    assert data["username"] == "newuser"
    assert "id" in data
    assert "hashed_password" not in data  # No debe exponer password


@pytest.mark.integration
def test_register_duplicate_email(client, test_user):
    """Test que no permite email duplicado"""
    response = client.post(
        "/api/auth/register",
        json={
            "email": "test@example.com",  # Ya existe
            "username": "anotheruser",
            "password": "password123"
        }
    )
    
    assert response.status_code == 400
    assert "already registered" in response.json()["detail"].lower()


@pytest.mark.integration
def test_register_duplicate_username(client, test_user):
    """Test que no permite username duplicado"""
    response = client.post(
        "/api/auth/register",
        json={
            "email": "another@example.com",
            "username": "testuser",  # Ya existe
            "password": "password123"
        }
    )
    
    assert response.status_code == 400
    assert "already" in response.json()["detail"].lower()


@pytest.mark.integration
def test_login_success(client, test_user):
    """Test de login exitoso"""
    response = client.post(
        "/api/auth/login",
        data={
            "username": "testuser",
            "password": "testpassword123"
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


@pytest.mark.integration
def test_login_wrong_password(client, test_user):
    """Test de login con contraseña incorrecta"""
    response = client.post(
        "/api/auth/login",
        data={
            "username": "testuser",
            "password": "wrongpassword"
        }
    )
    
    assert response.status_code == 401
    assert "incorrect" in response.json()["detail"].lower()


@pytest.mark.integration
def test_login_nonexistent_user(client):
    """Test de login con usuario inexistente"""
    response = client.post(
        "/api/auth/login",
        data={
            "username": "nonexistent",
            "password": "password123"
        }
    )
    
    assert response.status_code == 401


@pytest.mark.integration
def test_get_current_user(client, auth_headers):
    """Test para obtener usuario actual autenticado"""
    response = client.get(
        "/api/auth/me",
        headers=auth_headers
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser"
    assert data["email"] == "test@example.com"


@pytest.mark.integration
def test_get_current_user_unauthorized(client):
    """Test para obtener usuario sin autenticación"""
    response = client.get("/api/auth/me")
    
    assert response.status_code == 401


@pytest.mark.integration
def test_get_current_user_invalid_token(client):
    """Test con token inválido"""
    response = client.get(
        "/api/auth/me",
        headers={"Authorization": "Bearer invalid_token"}
    )
    
    assert response.status_code == 401

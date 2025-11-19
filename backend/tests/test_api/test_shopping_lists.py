"""
Tests para API de listas de compras
"""
import pytest


@pytest.mark.integration
def test_create_shopping_list(client, auth_headers):
    """Test para crear nueva lista de compras"""
    new_list = {
        "name": "Lista Semanal",
        "budget": 15000.0
    }
    
    response = client.post(
        "/api/shopping-lists/",
        json=new_list,
        headers=auth_headers
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Lista Semanal"
    assert data["budget"] == 15000.0
    assert "id" in data


@pytest.mark.integration
def test_get_all_shopping_lists(client, sample_shopping_list, auth_headers):
    """Test para obtener todas las listas del usuario"""
    response = client.get("/api/shopping-lists/", headers=auth_headers)
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    assert data[0]["name"] == "Lista Test"


@pytest.mark.integration
def test_get_shopping_list_by_id(client, sample_shopping_list, auth_headers):
    """Test para obtener lista específica con items"""
    list_id = sample_shopping_list.id
    
    response = client.get(f"/api/shopping-lists/{list_id}", headers=auth_headers)
    
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == list_id
    assert data["name"] == "Lista Test"
    assert "items" in data
    assert len(data["items"]) == 3  # 3 productos en sample_products
    assert "total_cost" in data
    assert "total_eco_score" in data


@pytest.mark.integration
def test_get_shopping_list_not_found(client, auth_headers):
    """Test para lista inexistente"""
    response = client.get("/api/shopping-lists/99999", headers=auth_headers)
    
    assert response.status_code == 404


@pytest.mark.integration
def test_update_budget(client, sample_shopping_list, auth_headers):
    """Test para actualizar presupuesto de lista"""
    list_id = sample_shopping_list.id
    
    response = client.patch(
        f"/api/shopping-lists/{list_id}",
        json={"budget": 20000.0},
        headers=auth_headers
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["budget"] == 20000.0


@pytest.mark.integration
def test_add_item_to_list(client, sample_shopping_list, sample_products, auth_headers):
    """Test para agregar producto a lista"""
    list_id = sample_shopping_list.id
    product_id = sample_products[0].id
    
    response = client.post(
        f"/api/shopping-lists/{list_id}/items",
        json={
            "product_id": product_id,
            "quantity": 3
        },
        headers=auth_headers
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Item added successfully"


@pytest.mark.integration
def test_update_item_quantity(client, sample_shopping_list, auth_headers, db):
    """Test para actualizar cantidad de item"""
    list_id = sample_shopping_list.id
    # Obtener primer item
    item = sample_shopping_list.items[0]
    item_id = item.id
    
    response = client.patch(
        f"/api/shopping-lists/{list_id}/items/{item_id}",
        json={"quantity": 5},
        headers=auth_headers
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["quantity"] == 5


@pytest.mark.integration
def test_delete_item_from_list(client, sample_shopping_list, auth_headers):
    """Test para eliminar item de lista"""
    list_id = sample_shopping_list.id
    item_id = sample_shopping_list.items[0].id
    
    response = client.delete(
        f"/api/shopping-lists/{list_id}/items/{item_id}",
        headers=auth_headers
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Item deleted successfully"


@pytest.mark.integration
def test_optimize_shopping_list(client, sample_shopping_list, auth_headers):
    """Test para optimizar lista de compras"""
    list_id = sample_shopping_list.id
    
    response = client.post(
        f"/api/shopping-lists/{list_id}/optimize",
        headers=auth_headers
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "selected_items" in data
    assert "total_cost" in data
    assert "total_eco_score" in data
    assert "optimization_details" in data
    assert data["total_cost"] <= 10000.0  # Budget de sample_shopping_list


@pytest.mark.integration
def test_substitute_products(client, sample_shopping_list, auth_headers):
    """Test para buscar sustituciones"""
    list_id = sample_shopping_list.id
    
    response = client.post(
        f"/api/shopping-lists/{list_id}/substitute",
        headers=auth_headers
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "substitutions" in data
    assert isinstance(data["substitutions"], list)


@pytest.mark.integration
def test_delete_shopping_list(client, sample_shopping_list, auth_headers):
    """Test para eliminar lista"""
    list_id = sample_shopping_list.id
    
    response = client.delete(
        f"/api/shopping-lists/{list_id}",
        headers=auth_headers
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Shopping list deleted successfully"
    
    # Verificar que no existe
    response = client.get(f"/api/shopping-lists/{list_id}", headers=auth_headers)
    assert response.status_code == 404


@pytest.mark.integration
def test_shopping_list_unauthorized(client, sample_shopping_list):
    """Test que requiere autenticación"""
    response = client.get("/api/shopping-lists/")
    
    assert response.status_code == 401


@pytest.mark.integration
def test_cannot_access_other_user_list(client, sample_shopping_list, db):
    """Test que un usuario no puede acceder a lista de otro usuario"""
    # Crear otro usuario
    from app.models.models import User
    from app.api.auth import get_password_hash
    
    other_user = User(
        email="other@example.com",
        username="otheruser",
        hashed_password=get_password_hash("password123")
    )
    db.add(other_user)
    db.commit()
    
    # Login como otro usuario
    response = client.post(
        "/api/auth/login",
        data={"username": "otheruser", "password": "password123"}
    )
    other_token = response.json()["access_token"]
    other_headers = {"Authorization": f"Bearer {other_token}"}
    
    # Intentar acceder a lista del primer usuario
    list_id = sample_shopping_list.id
    response = client.get(
        f"/api/shopping-lists/{list_id}",
        headers=other_headers
    )
    
    assert response.status_code == 403  # Forbidden

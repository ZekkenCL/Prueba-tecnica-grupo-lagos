"""
Tests para API de productos
"""
import pytest


@pytest.mark.integration
def test_get_all_products(client, sample_products, auth_headers):
    """Test para obtener todos los productos"""
    response = client.get("/api/products/", headers=auth_headers)
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3
    assert data[0]["name"] == "Leche Colun Entera"


@pytest.mark.integration
def test_get_products_with_search(client, sample_products, auth_headers):
    """Test de búsqueda de productos"""
    response = client.get(
        "/api/products/",
        params={"search": "Leche"},
        headers=auth_headers
    )
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    assert "Leche" in data[0]["name"]


@pytest.mark.integration
def test_get_products_with_category_filter(client, sample_products, auth_headers):
    """Test de filtro por categoría"""
    response = client.get(
        "/api/products/",
        params={"category": "Lácteos"},
        headers=auth_headers
    )
    
    assert response.status_code == 200
    data = response.json()
    assert all(p["category"] == "Lácteos" for p in data)


@pytest.mark.integration
def test_get_products_with_min_eco_score(client, sample_products, auth_headers):
    """Test de filtro por eco_score mínimo"""
    response = client.get(
        "/api/products/",
        params={"min_eco_score": 70},
        headers=auth_headers
    )
    
    assert response.status_code == 200
    data = response.json()
    assert all(p["eco_score"] >= 70 for p in data)


@pytest.mark.integration
def test_get_product_by_id(client, sample_products, auth_headers):
    """Test para obtener producto por ID"""
    product_id = sample_products[0].id
    
    response = client.get(f"/api/products/{product_id}", headers=auth_headers)
    
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == product_id
    assert data["name"] == "Leche Colun Entera"


@pytest.mark.integration
def test_get_product_not_found(client, auth_headers):
    """Test para producto inexistente"""
    response = client.get("/api/products/99999", headers=auth_headers)
    
    assert response.status_code == 404


@pytest.mark.integration
def test_get_product_sustainability(client, sample_products, auth_headers):
    """Test para obtener análisis de sostenibilidad"""
    product_id = sample_products[0].id
    
    response = client.get(
        f"/api/products/{product_id}/sustainability",
        headers=auth_headers
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "total_score" in data
    assert "economic_score" in data
    assert "environmental_score" in data
    assert "social_score" in data
    assert "breakdown" in data


@pytest.mark.integration
def test_get_product_substitutes(client, sample_products, auth_headers):
    """Test para obtener alternativas de producto"""
    product_id = sample_products[0].id
    
    response = client.get(
        f"/api/products/{product_id}/substitutes",
        headers=auth_headers
    )
    
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


@pytest.mark.integration
def test_get_categories(client, sample_products, auth_headers):
    """Test para obtener todas las categorías"""
    response = client.get("/api/products/categories", headers=auth_headers)
    
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0


@pytest.mark.integration
def test_create_product(client, auth_headers):
    """Test para crear nuevo producto"""
    new_product = {
        "barcode": "7802900000099",
        "name": "Producto Nuevo",
        "brand": "Marca Test",
        "category": "Test",
        "price": 1500.0,
        "unit": "unidad",
        "eco_score": 75.0,
        "carbon_footprint": 1.0,
        "water_usage": 100.0,
        "packaging_score": 70.0,
        "social_score": 75.0,
        "calories": 200.0,
        "protein": 10.0,
        "fat": 5.0,
        "carbs": 30.0
    }
    
    response = client.post(
        "/api/products/",
        json=new_product,
        headers=auth_headers
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Producto Nuevo"
    assert data["price"] == 1500.0
    assert "id" in data


@pytest.mark.integration
def test_get_products_unauthorized(client, sample_products):
    """Test que verifica que la lista de productos es pública (no requiere autenticación)"""
    response = client.get("/api/products/")
    
    # Los productos deben ser accesibles sin autenticación
    assert response.status_code == 200
    assert len(response.json()) > 0

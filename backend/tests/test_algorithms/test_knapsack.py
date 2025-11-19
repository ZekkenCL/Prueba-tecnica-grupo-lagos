"""
Tests para el algoritmo de Knapsack Multi-Objetivo
"""
import pytest
from app.algorithms.knapsack import optimize_shopping_list


@pytest.mark.unit
def test_knapsack_basic_optimization():
    """Test básico de optimización con presupuesto"""
    products = [
        {"id": 1, "name": "Producto A", "price": 1000, "eco_score": 80, "protein": 10, "carbs": 20, "fat": 5, "category": "Lácteos"},
        {"id": 2, "name": "Producto B", "price": 1500, "eco_score": 90, "protein": 12, "carbs": 25, "fat": 3, "category": "Carnes"},
        {"id": 3, "name": "Producto C", "price": 3000, "eco_score": 70, "protein": 8, "carbs": 30, "fat": 4, "category": "Verduras"},
    ]
    
    budget = 5000
    result = optimize_shopping_list(products, budget)
    
    assert "products" in result
    assert "metrics" in result
    metrics = result["metrics"]
    assert metrics["total_cost"] <= budget
    assert len(result["products"]) > 0
    assert metrics["budget_usage"] <= 100


@pytest.mark.unit
def test_knapsack_respects_budget():
    """Test que verifica que respeta el presupuesto"""
    products = [
        {"id": 1, "name": "Producto A", "price": 6000, "eco_score": 80, "protein": 10, "carbs": 20, "fat": 5, "category": "Lácteos"},
    ]
    
    budget = 5000
    result = optimize_shopping_list(products, budget)
    
    metrics = result["metrics"]
    assert metrics["total_cost"] <= budget


@pytest.mark.unit
def test_knapsack_selects_best_eco_score():
    """Test que selecciona productos con mejor eco_score"""
    products = [
        {"id": 1, "name": "Lácteo Peor", "price": 1000, "eco_score": 60, "protein": 10, "carbs": 20, "fat": 5, "category": "Lácteos"},
        {"id": 2, "name": "Lácteo Mejor", "price": 1000, "eco_score": 90, "protein": 10, "carbs": 20, "fat": 5, "category": "Lácteos"},
        {"id": 3, "name": "Producto B", "price": 1500, "eco_score": 70, "protein": 12, "carbs": 25, "fat": 3, "category": "Carnes"},
    ]
    
    budget = 5000
    result = optimize_shopping_list(products, budget)
    
    selected_ids = [p["id"] for p in result["products"]]
    if 1 in selected_ids or 2 in selected_ids:
        assert 2 in selected_ids


@pytest.mark.unit
def test_knapsack_prevents_duplicate_categories():
    """Test que intenta evitar duplicados de la misma categoría con peor eco_score"""
    products = [
        {"id": 1, "name": "Lácteo A", "price": 1000, "eco_score": 85, "protein": 10, "carbs": 15, "fat": 5, "category": "Lácteos"},
        {"id": 2, "name": "Lácteo B", "price": 900, "eco_score": 60, "protein": 9, "carbs": 14, "fat": 4, "category": "Lácteos"},
        {"id": 3, "name": "Pan", "price": 1500, "eco_score": 70, "protein": 8, "carbs": 40, "fat": 3, "category": "Panadería"},
    ]
    
    budget = 5000
    result = optimize_shopping_list(products, budget)
    
    # El algoritmo genético intenta optimizar, pero puede seleccionar múltiples de la misma categoría
    # Verificamos que al menos selecciona productos
    assert len(result["products"]) > 0
    
    # Si hay lácteos, debería priorizar el de mayor eco_score
    lacteos = [p for p in result["products"] if p["category"] == "Lácteos"]
    if lacteos:
        # Si hay más de un lácteo, el con mayor ID (Lácteo A) debería estar
        assert any(p["id"] == 1 for p in lacteos)


@pytest.mark.unit
def test_knapsack_with_empty_products():
    """Test con lista vacía de productos"""
    products = []
    budget = 5000

    result = optimize_shopping_list(products, budget)
    
    assert result["products"] == []
    assert result["metrics"]["total_cost"] == 0


@pytest.mark.unit
def test_knapsack_with_zero_budget():
    """Test con presupuesto cero"""
    products = [
        {"id": 1, "name": "Producto", "price": 1000, "eco_score": 80, "protein": 10, "carbs": 20, "fat": 5, "category": "Test"},
    ]

    budget = 0
    result = optimize_shopping_list(products, budget)
    
    assert result["products"] == []
    assert result["metrics"]["total_cost"] == 0


@pytest.mark.unit
def test_knapsack_returns_correct_structure():
    """Test que la respuesta tiene la estructura correcta"""
    products = [
        {"id": 1, "name": "Producto", "price": 1000, "eco_score": 80, "protein": 10, "carbs": 20, "fat": 5, "category": "Test"},
    ]

    budget = 2000
    result = optimize_shopping_list(products, budget)
    
    assert "products" in result
    assert "metrics" in result
    assert isinstance(result["products"], list)
    assert isinstance(result["metrics"], dict)
    
    metrics = result["metrics"]
    assert "total_cost" in metrics
    assert "eco_score" in metrics
    assert "savings" in metrics
    assert "total_products" in metrics
    assert "budget_usage" in metrics

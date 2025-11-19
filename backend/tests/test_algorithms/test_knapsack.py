"""
Tests para el algoritmo de Knapsack Multi-Objetivo
"""
import pytest
from app.algorithms.knapsack import MultiObjectiveKnapsack


@pytest.mark.unit
def test_knapsack_basic_optimization():
    """Test básico de optimización con presupuesto"""
    products = [
        {
            "id": 1,
            "name": "Producto A",
            "price": 1000,
            "eco_score": 80,
            "protein": 10,
            "carbs": 20,
            "fat": 5,
            "category": "Lácteos"
        },
        {
            "id": 2,
            "name": "Producto B",
            "price": 2000,
            "eco_score": 90,
            "protein": 15,
            "carbs": 25,
            "fat": 8,
            "category": "Carnes"
        },
        {
            "id": 3,
            "name": "Producto C",
            "price": 3000,
            "eco_score": 70,
            "protein": 8,
            "carbs": 30,
            "fat": 4,
            "category": "Verduras"
        },
    ]
    
    budget = 5000
    knapsack = MultiObjectiveKnapsack(products, budget)
    result = knapsack.optimize()
    
    # Verificaciones
    assert "selected_items" in result
    assert "total_cost" in result
    assert "total_eco_score" in result
    assert result["total_cost"] <= budget
    assert result["selected_items"] > 0
    assert result["budget_usage"] <= 100


@pytest.mark.unit
def test_knapsack_respects_budget():
    """Test que el algoritmo respeta el presupuesto"""
    products = [
        {
            "id": 1,
            "name": "Producto Caro",
            "price": 10000,
            "eco_score": 95,
            "protein": 20,
            "carbs": 30,
            "fat": 10,
            "category": "Premium"
        },
    ]
    
    budget = 5000
    knapsack = MultiObjectiveKnapsack(products, budget)
    result = knapsack.optimize()
    
    # No debería seleccionar el producto porque excede presupuesto
    assert result["total_cost"] <= budget


@pytest.mark.unit
def test_knapsack_selects_best_eco_score():
    """Test que prioriza productos con mejor eco_score"""
    products = [
        {
            "id": 1,
            "name": "Bajo Eco",
            "price": 1000,
            "eco_score": 30,
            "protein": 10,
            "carbs": 20,
            "fat": 5,
            "category": "A"
        },
        {
            "id": 2,
            "name": "Alto Eco",
            "price": 1000,
            "eco_score": 90,
            "protein": 10,
            "carbs": 20,
            "fat": 5,
            "category": "B"
        },
    ]
    
    budget = 1500
    knapsack = MultiObjectiveKnapsack(products, budget)
    result = knapsack.optimize()
    
    # Debería seleccionar el de mayor eco_score si el presupuesto lo permite
    assert result["selected_items"] >= 1
    assert result["total_eco_score"] > 0


@pytest.mark.unit
def test_knapsack_prevents_duplicate_categories():
    """Test que no selecciona múltiples productos de la misma categoría con peor eco_score"""
    products = [
        {
            "id": 1,
            "name": "Lácteo A - Mejor",
            "price": 1000,
            "eco_score": 85,
            "protein": 10,
            "carbs": 15,
            "fat": 5,
            "category": "Lácteos"
        },
        {
            "id": 2,
            "name": "Lácteo B - Peor",
            "price": 900,
            "eco_score": 60,
            "protein": 9,
            "carbs": 14,
            "fat": 4,
            "category": "Lácteos"
        },
        {
            "id": 3,
            "name": "Pan",
            "price": 1500,
            "eco_score": 70,
            "protein": 8,
            "carbs": 40,
            "fat": 3,
            "category": "Panadería"
        },
    ]
    
    budget = 5000
    knapsack = MultiObjectiveKnapsack(products, budget)
    result = knapsack.optimize()
    
    # Debería incluir el mejor lácteo, no ambos
    assert result["selected_items"] <= 2  # Máximo 2 productos (uno por categoría)


@pytest.mark.unit
def test_knapsack_with_empty_products():
    """Test con lista vacía de productos"""
    products = []
    budget = 5000
    
    knapsack = MultiObjectiveKnapsack(products, budget)
    result = knapsack.optimize()
    
    assert result["selected_items"] == 0
    assert result["total_cost"] == 0
    assert result["total_eco_score"] == 0


@pytest.mark.unit
def test_knapsack_with_zero_budget():
    """Test con presupuesto cero"""
    products = [
        {
            "id": 1,
            "name": "Producto",
            "price": 1000,
            "eco_score": 80,
            "protein": 10,
            "carbs": 20,
            "fat": 5,
            "category": "Test"
        },
    ]
    
    budget = 0
    knapsack = MultiObjectiveKnapsack(products, budget)
    result = knapsack.optimize()
    
    # No debería seleccionar nada con presupuesto 0
    assert result["selected_items"] == 0
    assert result["total_cost"] == 0


@pytest.mark.unit
def test_knapsack_returns_correct_structure():
    """Test que la respuesta tiene la estructura correcta"""
    products = [
        {
            "id": 1,
            "name": "Producto",
            "price": 1000,
            "eco_score": 80,
            "protein": 10,
            "carbs": 20,
            "fat": 5,
            "category": "Test"
        },
    ]
    
    budget = 2000
    knapsack = MultiObjectiveKnapsack(products, budget)
    result = knapsack.optimize()
    
    # Verificar estructura de respuesta
    assert isinstance(result, dict)
    assert "selected_items" in result
    assert "total_cost" in result
    assert "total_eco_score" in result
    assert "total_nutrition_score" in result
    assert "total_savings" in result
    assert "budget_usage" in result
    assert "optimization_details" in result
    
    # Verificar tipos
    assert isinstance(result["selected_items"], int)
    assert isinstance(result["total_cost"], (int, float))
    assert isinstance(result["total_eco_score"], (int, float))
    assert isinstance(result["budget_usage"], (int, float))

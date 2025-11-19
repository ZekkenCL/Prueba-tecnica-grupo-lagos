"""
Tests para el algoritmo de sustitución de productos
"""
import pytest
from app.algorithms.substitution import find_product_substitutes


@pytest.mark.unit
def test_find_substitutes_same_category():
    """Test que solo encuentra sustitutos de la misma categoría"""
    target_product = {
        "id": 1,
        "name": "Leche Colun",
        "category": "Lácteos",
        "price": 1000,
        "eco_score": 70
    }
    
    all_products = [
        target_product,
        {
            "id": 2,
            "name": "Leche Soprole",
            "category": "Lácteos",
            "price": 1100,
            "eco_score": 85  # Mejor eco_score
        },
        {
            "id": 3,
            "name": "Pan",
            "category": "Panadería",
            "price": 900,
            "eco_score": 90  # Mejor score pero diferente categoría
        }
    ]
    
    substitutes = find_product_substitutes(target_product, all_products)
    
    # Solo debería devolver productos de la misma categoría
    for sub in substitutes:
        assert sub["category"] == "Lácteos"
    
    # No debería incluir el producto original
    substitute_ids = [s["id"] for s in substitutes]
    assert target_product["id"] not in substitute_ids


@pytest.mark.unit
def test_find_substitutes_better_eco_score():
    """Test que solo devuelve productos con mejor eco_score"""
    target_product = {
        "id": 1,
        "name": "Producto Base",
        "category": "Lácteos",
        "price": 1000,
        "eco_score": 70
    }
    
    all_products = [
        target_product,
        {
            "id": 2,
            "name": "Producto Mejor",
            "category": "Lácteos",
            "price": 1000,
            "eco_score": 80  # Mejor
        },
        {
            "id": 3,
            "name": "Producto Peor",
            "category": "Lácteos",
            "price": 1000,
            "eco_score": 60  # Peor
        }
    ]
    
    substitutes = find_product_substitutes(
        target_product, 
        all_products,
        min_score_improvement=5.0
    )
    
    # Todos los sustitutos deben tener mejor eco_score
    for sub in substitutes:
        assert sub["eco_score"] > target_product["eco_score"]


@pytest.mark.unit
def test_find_substitutes_price_limit():
    """Test que respeta el límite de precio (max_price_increase)"""
    target_product = {
        "id": 1,
        "name": "Producto Base",
        "category": "Lácteos",
        "price": 1000,
        "eco_score": 70
    }
    
    all_products = [
        target_product,
        {
            "id": 2,
            "name": "Producto OK",
            "category": "Lácteos",
            "price": 1300,  # +30% (dentro del límite 35%)
            "eco_score": 85
        },
        {
            "id": 3,
            "name": "Producto Muy Caro",
            "category": "Lácteos",
            "price": 1500,  # +50% (excede el límite)
            "eco_score": 95
        }
    ]
    
    substitutes = find_product_substitutes(
        target_product, 
        all_products,
        max_price_increase=0.35  # 35%
    )
    
    # Solo debería incluir el producto OK
    assert len(substitutes) == 1
    assert substitutes[0]["id"] == 2


@pytest.mark.unit
def test_find_substitutes_min_score_improvement():
    """Test del parámetro min_score_improvement"""
    target_product = {
        "id": 1,
        "name": "Producto Base",
        "category": "Lácteos",
        "price": 1000,
        "eco_score": 70
    }
    
    all_products = [
        target_product,
        {
            "id": 2,
            "name": "Mejora Pequeña",
            "category": "Lácteos",
            "price": 1000,
            "eco_score": 72  # +2 puntos
        },
        {
            "id": 3,
            "name": "Mejora Grande",
            "category": "Lácteos",
            "price": 1000,
            "eco_score": 85  # +15 puntos
        }
    ]
    
    # Con min_score_improvement=5.0, solo debería devolver el de mejora grande
    substitutes = find_product_substitutes(
        target_product, 
        all_products,
        min_score_improvement=5.0
    )
    
    assert len(substitutes) == 1
    assert substitutes[0]["id"] == 3


@pytest.mark.unit
def test_find_substitutes_no_results():
    """Test cuando no hay sustitutos disponibles"""
    target_product = {
        "id": 1,
        "name": "Producto Único",
        "category": "Lácteos",
        "price": 1000,
        "eco_score": 95  # Ya es el mejor
    }
    
    all_products = [
        target_product,
        {
            "id": 2,
            "name": "Producto Peor",
            "category": "Lácteos",
            "price": 1000,
            "eco_score": 70  # Peor score
        }
    ]
    
    substitutes = find_product_substitutes(target_product, all_products)
    
    # No debería encontrar sustitutos
    assert len(substitutes) == 0


@pytest.mark.unit
def test_find_substitutes_sorted_by_eco_score():
    """Test que los resultados están ordenados por eco_score descendente"""
    target_product = {
        "id": 1,
        "name": "Producto Base",
        "category": "Lácteos",
        "price": 1000,
        "eco_score": 60
    }
    
    all_products = [
        target_product,
        {
            "id": 2,
            "name": "Opción 1",
            "category": "Lácteos",
            "price": 1000,
            "eco_score": 75
        },
        {
            "id": 3,
            "name": "Opción 2",
            "category": "Lácteos",
            "price": 1000,
            "eco_score": 90
        },
        {
            "id": 4,
            "name": "Opción 3",
            "category": "Lácteos",
            "price": 1000,
            "eco_score": 80
        }
    ]
    
    substitutes = find_product_substitutes(
        target_product, 
        all_products,
        max_results=3
    )
    
    # Verificar orden descendente por eco_score
    for i in range(len(substitutes) - 1):
        assert substitutes[i]["eco_score"] >= substitutes[i + 1]["eco_score"]


@pytest.mark.unit
def test_find_substitutes_max_results():
    """Test del parámetro max_results"""
    target_product = {
        "id": 1,
        "name": "Producto Base",
        "category": "Lácteos",
        "price": 1000,
        "eco_score": 60
    }
    
    all_products = [target_product]
    
    # Agregar 10 productos mejores
    for i in range(10):
        all_products.append({
            "id": i + 2,
            "name": f"Opción {i+1}",
            "category": "Lácteos",
            "price": 1000,
            "eco_score": 70 + i
        })
    
    # Pedir máximo 3 resultados
    substitutes = find_product_substitutes(
        target_product, 
        all_products,
        max_results=3
    )
    
    assert len(substitutes) == 3


@pytest.mark.unit
def test_find_substitutes_with_empty_list():
    """Test con lista vacía de productos"""
    target_product = {
        "id": 1,
        "name": "Producto Solo",
        "category": "Lácteos",
        "price": 1000,
        "eco_score": 70
    }
    
    all_products = []
    
    substitutes = find_product_substitutes(target_product, all_products)
    
    assert len(substitutes) == 0

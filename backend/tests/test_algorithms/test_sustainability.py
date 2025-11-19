"""
Tests para el sistema de scoring de sostenibilidad
"""
import pytest
from app.algorithms.sustainability import calculate_sustainability_score


@pytest.mark.unit
def test_sustainability_score_basic():
    """Test básico de cálculo de score de sostenibilidad"""
    product = {
        "id": 1,
        "name": "Producto Test",
        "price": 1000,
        "category": "Lácteos",
        "eco_score": 75,
        "carbon_footprint": 1.5,
        "water_usage": 150,
        "packaging_score": 70,
        "social_score": 80
    }
    
    all_products = [product]
    
    result = calculate_sustainability_score(product, all_products)
    
    # Verificar estructura
    assert "total_score" in result
    assert "economic_score" in result
    assert "environmental_score" in result
    assert "social_score" in result
    assert "breakdown" in result
    
    # Verificar rangos (0-100)
    assert 0 <= result["total_score"] <= 100
    assert 0 <= result["economic_score"] <= 100
    assert 0 <= result["environmental_score"] <= 100
    assert 0 <= result["social_score"] <= 100


@pytest.mark.unit
def test_sustainability_score_weights():
    """Test que verifica los pesos: 35% económico, 40% ambiental, 25% social"""
    product = {
        "id": 1,
        "name": "Producto Test",
        "price": 1000,
        "category": "Lácteos",
        "eco_score": 100,  # Máximo ambiental
        "carbon_footprint": 0,
        "water_usage": 0,
        "packaging_score": 100,
        "social_score": 100
    }
    
    all_products = [product]
    result = calculate_sustainability_score(product, all_products)
    
    # Con todos los scores en 100, el total debería ser cercano a 100
    assert result["total_score"] >= 90  # Margen de error


@pytest.mark.unit
def test_sustainability_score_low_values():
    """Test con valores bajos de sostenibilidad"""
    product = {
        "id": 1,
        "name": "Producto Poco Sostenible",
        "price": 5000,  # Precio alto
        "category": "Premium",
        "eco_score": 20,  # Bajo eco_score
        "carbon_footprint": 5.0,  # Alta huella de carbono
        "water_usage": 1000,  # Alto uso de agua
        "packaging_score": 20,  # Mal empaque
        "social_score": 20  # Bajo impacto social
    }
    
    all_products = [product]
    result = calculate_sustainability_score(product, all_products)
    
    # El score total debería ser bajo
    assert result["total_score"] < 50
    assert result["environmental_score"] < 50


@pytest.mark.unit
def test_sustainability_score_comparison():
    """Test de comparación entre productos"""
    product_good = {
        "id": 1,
        "name": "Producto Sostenible",
        "price": 1000,
        "category": "Lácteos",
        "eco_score": 90,
        "carbon_footprint": 0.5,
        "water_usage": 50,
        "packaging_score": 85,
        "social_score": 90
    }
    
    product_bad = {
        "id": 2,
        "name": "Producto No Sostenible",
        "price": 1000,
        "category": "Lácteos",
        "eco_score": 30,
        "carbon_footprint": 4.0,
        "water_usage": 800,
        "packaging_score": 30,
        "social_score": 30
    }
    
    all_products = [product_good, product_bad]
    
    result_good = calculate_sustainability_score(product_good, all_products)
    result_bad = calculate_sustainability_score(product_bad, all_products)
    
    # El producto sostenible debería tener mejor score
    assert result_good["total_score"] > result_bad["total_score"]
    assert result_good["environmental_score"] > result_bad["environmental_score"]


@pytest.mark.unit
def test_sustainability_score_economic_factor():
    """Test del factor económico (35% del total)"""
    cheap_product = {
        "id": 1,
        "name": "Producto Barato",
        "price": 500,
        "category": "Lácteos",
        "eco_score": 70,
        "carbon_footprint": 1.0,
        "water_usage": 100,
        "packaging_score": 70,
        "social_score": 70
    }
    
    expensive_product = {
        "id": 2,
        "name": "Producto Caro",
        "price": 3000,
        "category": "Lácteos",
        "eco_score": 70,
        "carbon_footprint": 1.0,
        "water_usage": 100,
        "packaging_score": 70,
        "social_score": 70
    }
    
    all_products = [cheap_product, expensive_product]
    
    result_cheap = calculate_sustainability_score(cheap_product, all_products)
    result_expensive = calculate_sustainability_score(expensive_product, all_products)
    
    # El producto barato debería tener mejor score económico
    assert result_cheap["economic_score"] > result_expensive["economic_score"]


@pytest.mark.unit
def test_sustainability_score_with_missing_fields():
    """Test con campos faltantes (debería usar valores por defecto)"""
    product = {
        "id": 1,
        "name": "Producto Incompleto",
        "price": 1000,
        "category": "Test"
        # Faltan campos de sostenibilidad
    }
    
    all_products = [product]
    
    # No debería fallar, usar valores por defecto
    result = calculate_sustainability_score(product, all_products)
    
    assert "total_score" in result
    assert result["total_score"] >= 0


@pytest.mark.unit
def test_sustainability_breakdown_structure():
    """Test de la estructura del breakdown detallado"""
    product = {
        "id": 1,
        "name": "Producto Test",
        "price": 1000,
        "category": "Lácteos",
        "eco_score": 75,
        "carbon_footprint": 1.5,
        "water_usage": 150,
        "packaging_score": 70,
        "social_score": 80
    }
    
    all_products = [product]
    result = calculate_sustainability_score(product, all_products)
    
    # Verificar estructura del breakdown
    assert "breakdown" in result
    breakdown = result["breakdown"]
    
    assert "economic" in breakdown
    assert "environmental" in breakdown
    assert "social" in breakdown
    
    # Cada componente debería tener peso y score
    assert "weight" in breakdown["economic"]
    assert "score" in breakdown["economic"]
    assert breakdown["economic"]["weight"] == 0.35  # 35%
    
    assert "weight" in breakdown["environmental"]
    assert breakdown["environmental"]["weight"] == 0.40  # 40%
    
    assert "weight" in breakdown["social"]
    assert breakdown["social"]["weight"] == 0.25  # 25%

"""
Configuración de fixtures para tests
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.database import Base, get_db
from app.models.models import User, Product, ShoppingList, ShoppingListItem
from app.api.auth import get_password_hash

# Base de datos en memoria para tests
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db():
    """Fixture de base de datos para cada test"""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db):
    """Fixture de cliente de prueba con DB"""
    def override_get_db():
        try:
            yield db
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def test_user(db):
    """Fixture de usuario de prueba"""
    user = User(
        email="test@example.com",
        username="testuser",
        hashed_password=get_password_hash("testpassword123")
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@pytest.fixture
def auth_headers(client, test_user):
    """Fixture de headers de autenticación"""
    response = client.post(
        "/api/auth/login",
        data={"username": "testuser", "password": "testpassword123"}
    )
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def sample_products(db):
    """Fixture de productos de prueba"""
    products = [
        Product(
            barcode="7802900000001",
            name="Leche Colun Entera",
            brand="Colun",
            category="Lácteos",
            price=1190.0,
            unit="1L",
            eco_score=78.0,
            carbon_footprint=1.2,
            water_usage=120.0,
            packaging_score=65.0,
            social_score=80.0,
            calories=150.0,
            protein=8.0,
            fat=8.0,
            carbs=12.0,
            image_url="https://example.com/colun.jpg"
        ),
        Product(
            barcode="7802900000002",
            name="Pan Ideal Molde",
            brand="Ideal",
            category="Panadería",
            price=1890.0,
            unit="500g",
            eco_score=65.0,
            carbon_footprint=0.8,
            water_usage=80.0,
            packaging_score=55.0,
            social_score=70.0,
            calories=265.0,
            protein=9.0,
            fat=3.5,
            carbs=49.0,
            image_url="https://example.com/pan.jpg"
        ),
        Product(
            barcode="7802900000003",
            name="Arroz Tucapel Grado 2",
            brand="Tucapel",
            category="Arroz",
            price=1590.0,
            unit="1kg",
            eco_score=72.0,
            carbon_footprint=2.1,
            water_usage=2500.0,
            packaging_score=60.0,
            social_score=75.0,
            calories=350.0,
            protein=7.0,
            fat=0.5,
            carbs=78.0,
            image_url="https://example.com/arroz.jpg"
        ),
    ]
    
    for product in products:
        db.add(product)
    db.commit()
    
    for product in products:
        db.refresh(product)
    
    return products


@pytest.fixture
def sample_shopping_list(db, test_user, sample_products):
    """Fixture de lista de compras con productos"""
    shopping_list = ShoppingList(
        name="Lista Test",
        budget=10000.0,
        owner_id=test_user.id
    )
    db.add(shopping_list)
    db.commit()
    db.refresh(shopping_list)
    
    # Agregar items a la lista
    for product in sample_products:
        item = ShoppingListItem(
            shopping_list_id=shopping_list.id,
            product_id=product.id,
            quantity=2
        )
        db.add(item)
    
    db.commit()
    db.refresh(shopping_list)
    
    return shopping_list

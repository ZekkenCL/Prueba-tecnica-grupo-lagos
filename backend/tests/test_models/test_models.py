"""
Tests para modelos de la base de datos
"""
import pytest
from app.models.models import User, Product, ShoppingList, ShoppingListItem
from app.api.auth import get_password_hash, verify_password

# Nota: El modelo usa owner_id, no user_id


@pytest.mark.unit
def test_user_model_creation(db):
    """Test de creación de modelo User"""
    user = User(
        email="model@example.com",
        username="modeluser",
        hashed_password=get_password_hash("testpass")
    )
    
    db.add(user)
    db.commit()
    db.refresh(user)
    
    assert user.id is not None
    assert user.email == "model@example.com"
    assert user.username == "modeluser"
    assert verify_password("testpass", user.hashed_password)


@pytest.mark.unit
def test_product_model_creation(db):
    """Test de creación de modelo Product"""
    product = Product(
        barcode="1234567890",
        name="Test Product",
        brand="Test Brand",
        category="Test Category",
        price=1000.0,
        unit="unidad",
        eco_score=75.0,
        carbon_footprint=1.5,
        water_usage=100.0,
        packaging_score=70.0,
        social_score=80.0,
        calories=200.0,
        protein=10.0,
        fat=5.0,
        carbs=30.0
    )
    
    db.add(product)
    db.commit()
    db.refresh(product)
    
    assert product.id is not None
    assert product.name == "Test Product"
    assert product.price == 1000.0
    assert product.eco_score == 75.0


@pytest.mark.unit
def test_shopping_list_model_creation(db, test_user):
    """Test de creación de modelo ShoppingList"""
    shopping_list = ShoppingList(
        name="Test List",
        budget=10000.0,
        owner_id=test_user.id
    )
    
    db.add(shopping_list)
    db.commit()
    db.refresh(shopping_list)
    
    assert shopping_list.id is not None
    assert shopping_list.name == "Test List"
    assert shopping_list.budget == 10000.0
    assert shopping_list.owner_id == test_user.id


@pytest.mark.unit
def test_shopping_list_item_creation(db, test_user, sample_products):
    """Test de creación de modelo ShoppingListItem"""
    shopping_list = ShoppingList(
        name="Test List",
        budget=10000.0,
        owner_id=test_user.id
    )
    db.add(shopping_list)
    db.commit()
    db.refresh(shopping_list)
    
    item = ShoppingListItem(
        shopping_list_id=shopping_list.id,
        product_id=sample_products[0].id,
        quantity=2
    )
    
    db.add(item)
    db.commit()
    db.refresh(item)
    
    assert item.id is not None
    assert item.quantity == 2
    assert item.shopping_list_id == shopping_list.id
    assert item.product_id == sample_products[0].id


@pytest.mark.unit
def test_user_shopping_lists_relationship(db, test_user):
    """Test de relación User -> ShoppingLists"""
    list1 = ShoppingList(name="List 1", budget=5000, owner_id=test_user.id)
    list2 = ShoppingList(name="List 2", budget=8000, owner_id=test_user.id)
    
    db.add(list1)
    db.add(list2)
    db.commit()
    
    # Refrescar usuario para cargar relaciones
    db.refresh(test_user)
    
    assert len(test_user.shopping_lists) == 2


@pytest.mark.unit
def test_shopping_list_items_relationship(db, test_user, sample_products):
    """Test de relación ShoppingList -> Items"""
    shopping_list = ShoppingList(
        name="Test List",
        budget=10000.0,
        owner_id=test_user.id
    )
    db.add(shopping_list)
    db.commit()
    db.refresh(shopping_list)
    
    # Agregar 3 items
    for product in sample_products:
        item = ShoppingListItem(
            shopping_list_id=shopping_list.id,
            product_id=product.id,
            quantity=1
        )
        db.add(item)
    
    db.commit()
    db.refresh(shopping_list)
    
    assert len(shopping_list.items) == 3


@pytest.mark.unit
def test_product_unique_barcode(db):
    """Test que el código de barras debe ser único"""
    product1 = Product(
        barcode="1111111111",
        name="Product 1",
        category="Test",
        price=1000,
        eco_score=70
    )
    
    product2 = Product(
        barcode="1111111111",  # Mismo barcode
        name="Product 2",
        category="Test",
        price=2000,
        eco_score=80
    )
    
    db.add(product1)
    db.commit()
    
    db.add(product2)
    
    # Debería fallar por barcode duplicado
    with pytest.raises(Exception):
        db.commit()


@pytest.mark.unit
def test_user_unique_email(db):
    """Test que el email debe ser único"""
    user1 = User(
        email="unique@example.com",
        username="user1",
        hashed_password=get_password_hash("pass1")
    )
    
    user2 = User(
        email="unique@example.com",  # Mismo email
        username="user2",
        hashed_password=get_password_hash("pass2")
    )
    
    db.add(user1)
    db.commit()
    
    db.add(user2)
    
    # Debería fallar por email duplicado
    with pytest.raises(Exception):
        db.commit()


@pytest.mark.unit
def test_cascade_delete_shopping_list(db, test_user, sample_products):
    """Test que al eliminar lista se eliminan sus items"""
    shopping_list = ShoppingList(
        name="Test List",
        budget=10000.0,
        owner_id=test_user.id
    )
    db.add(shopping_list)
    db.commit()
    db.refresh(shopping_list)
    
    # Agregar items
    for product in sample_products:
        item = ShoppingListItem(
            shopping_list_id=shopping_list.id,
            product_id=product.id,
            quantity=1
        )
        db.add(item)
    db.commit()
    
    list_id = shopping_list.id
    
    # Eliminar lista
    db.delete(shopping_list)
    db.commit()
    
    # Verificar que items también fueron eliminados
    items = db.query(ShoppingListItem).filter_by(shopping_list_id=list_id).all()
    assert len(items) == 0

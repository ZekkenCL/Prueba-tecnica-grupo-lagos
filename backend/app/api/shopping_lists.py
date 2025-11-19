from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel

from app.database import get_db
from app.models.models import ShoppingList, ShoppingListItem, Product, User
from app.api.auth import get_current_user
from app.algorithms.knapsack import optimize_shopping_list
from app.algorithms.substitution import ProductSubstitution

router = APIRouter(prefix="/api/shopping-lists", tags=["shopping-lists"])

class ShoppingListCreate(BaseModel):
    name: str
    budget: Optional[float] = None

class ShoppingListItemCreate(BaseModel):
    product_id: int
    quantity: int = 1

class ShoppingListItemUpdate(BaseModel):
    quantity: int

class ShoppingListUpdate(BaseModel):
    name: Optional[str] = None
    budget: Optional[float] = None

class ShoppingListResponse(BaseModel):
    id: int
    name: str
    budget: Optional[float]
    is_optimized: bool
    total_cost: float
    total_savings: float
    total_eco_score: float
    total_carbon: float
    
    class Config:
        from_attributes = True

class ShoppingListDetailResponse(ShoppingListResponse):
    items: List[dict]

@router.get("/", response_model=List[ShoppingListResponse])
def get_shopping_lists(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    lists = db.query(ShoppingList).filter(ShoppingList.owner_id == current_user.id).all()
    return lists

@router.post("/", response_model=ShoppingListResponse)
def create_shopping_list(
    shopping_list: ShoppingListCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_list = ShoppingList(
        name=shopping_list.name,
        budget=shopping_list.budget,
        owner_id=current_user.id
    )
    db.add(db_list)
    db.commit()
    db.refresh(db_list)
    return db_list

@router.patch("/{list_id}")
def update_shopping_list(
    list_id: int,
    update_data: ShoppingListUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    shopping_list = db.query(ShoppingList).filter(
        ShoppingList.id == list_id,
        ShoppingList.owner_id == current_user.id
    ).first()
    
    if not shopping_list:
        raise HTTPException(status_code=404, detail="Shopping list not found")
    
    if update_data.budget is not None:
        if update_data.budget <= 0:
            raise HTTPException(status_code=400, detail="Budget must be greater than 0")
        shopping_list.budget = update_data.budget
    
    if update_data.name is not None:
        shopping_list.name = update_data.name
    
    db.commit()
    db.refresh(shopping_list)
    return {"message": "Shopping list updated", "budget": shopping_list.budget, "name": shopping_list.name}

@router.get("/{list_id}", response_model=ShoppingListDetailResponse)
def get_shopping_list(
    list_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    shopping_list = db.query(ShoppingList).filter(
        ShoppingList.id == list_id,
        ShoppingList.owner_id == current_user.id
    ).first()
    
    if not shopping_list:
        raise HTTPException(status_code=404, detail="Shopping list not found")
    
    # Obtener items con productos y CALCULAR totales en tiempo real
    items = []
    total_cost = 0
    total_eco_score = 0
    total_carbon = 0
    total_quantity = 0
    
    for item in shopping_list.items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        if product:
            subtotal = product.price * item.quantity
            total_cost += subtotal
            total_eco_score += product.eco_score  # Solo sumar el eco_score del producto
            total_carbon += (product.carbon_footprint or 0) * item.quantity
            total_quantity += item.quantity
            
            items.append({
                "id": item.id,
                "product": {
                    "id": product.id,
                    "name": product.name,
                    "brand": product.brand,
                    "price": product.price,
                    "eco_score": product.eco_score,
                    "image_url": product.image_url
                },
                "quantity": item.quantity,
                "is_substituted": item.is_substituted,
                "subtotal": subtotal
            })
    
    # Calcular eco-score promedio (por tipo de producto, no por cantidad)
    avg_eco_score = total_eco_score / len(items) if items else 0
    
    # Calcular ahorros vs presupuesto
    total_savings = (shopping_list.budget - total_cost) if shopping_list.budget else 0
    
    result = {
        "id": shopping_list.id,
        "name": shopping_list.name,
        "budget": shopping_list.budget,
        "is_optimized": shopping_list.is_optimized,
        "total_cost": round(total_cost, 2),
        "total_savings": round(total_savings, 2),
        "total_eco_score": round(avg_eco_score, 2),
        "total_carbon": round(total_carbon, 2),
        "items": items
    }
    
    return result

@router.post("/{list_id}/items")
def add_item_to_list(
    list_id: int,
    item: ShoppingListItemCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    shopping_list = db.query(ShoppingList).filter(
        ShoppingList.id == list_id,
        ShoppingList.owner_id == current_user.id
    ).first()
    
    if not shopping_list:
        raise HTTPException(status_code=404, detail="Shopping list not found")
    
    product = db.query(Product).filter(Product.id == item.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Verificar si ya existe
    existing = db.query(ShoppingListItem).filter(
        ShoppingListItem.shopping_list_id == list_id,
        ShoppingListItem.product_id == item.product_id
    ).first()
    
    if existing:
        existing.quantity += item.quantity
        db.commit()
        return {"message": "Quantity updated", "item_id": existing.id}
    
    db_item = ShoppingListItem(
        shopping_list_id=list_id,
        product_id=item.product_id,
        quantity=item.quantity
    )
    db.add(db_item)
    db.commit()
    
    return {"message": "Item added successfully", "item_id": db_item.id}

@router.patch("/{list_id}/items/{item_id}")
def update_item_quantity(
    list_id: int,
    item_id: int,
    update_data: ShoppingListItemUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    shopping_list = db.query(ShoppingList).filter(
        ShoppingList.id == list_id,
        ShoppingList.owner_id == current_user.id
    ).first()
    
    if not shopping_list:
        raise HTTPException(status_code=404, detail="Shopping list not found")
    
    item = db.query(ShoppingListItem).filter(
        ShoppingListItem.id == item_id,
        ShoppingListItem.shopping_list_id == list_id
    ).first()
    
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    if update_data.quantity < 1:
        raise HTTPException(status_code=400, detail="Quantity must be at least 1")
    
    item.quantity = update_data.quantity
    db.commit()
    db.refresh(item)
    
    return {"message": "Quantity updated", "quantity": item.quantity, "item_id": item.id}

@router.delete("/{list_id}/items/{item_id}")
def remove_item_from_list(
    list_id: int,
    item_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    shopping_list = db.query(ShoppingList).filter(
        ShoppingList.id == list_id,
        ShoppingList.owner_id == current_user.id
    ).first()
    
    if not shopping_list:
        raise HTTPException(status_code=404, detail="Shopping list not found")
    
    item = db.query(ShoppingListItem).filter(
        ShoppingListItem.id == item_id,
        ShoppingListItem.shopping_list_id == list_id
    ).first()
    
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    # Simplemente eliminar el item (los totales se calculan dinámicamente en GET)
    db.delete(item)
    db.commit()
    
    return {"message": "Item deleted successfully"}

@router.post("/{list_id}/optimize")
def optimize_list(
    list_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    shopping_list = db.query(ShoppingList).filter(
        ShoppingList.id == list_id,
        ShoppingList.owner_id == current_user.id
    ).first()
    
    if not shopping_list:
        raise HTTPException(status_code=404, detail="Shopping list not found")
    
    if not shopping_list.budget:
        raise HTTPException(status_code=400, detail="Budget is required for optimization")
    
    # Obtener productos de la lista
    current_products = []
    for item in shopping_list.items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        current_products.append({
            'id': product.id,
            'name': product.name,
            'price': product.price,
            'eco_score': product.eco_score,
            'protein': product.protein or 0,
            'calories': product.calories or 0,
            'fat': product.fat or 0,
            'quantity': item.quantity
        })
    
    # Obtener todos los productos disponibles
    all_products = db.query(Product).all()
    available_products = []
    for p in all_products:
        available_products.append({
            'id': p.id,
            'name': p.name,
            'price': p.price,
            'eco_score': p.eco_score,
            'protein': p.protein or 0,
            'calories': p.calories or 0,
            'fat': p.fat or 0,
            'category': p.category
        })
    
    # Optimizar
    required_ids = [p['id'] for p in current_products]
    result = optimize_shopping_list(available_products, shopping_list.budget, required_ids)
    
    # ELIMINAR items actuales
    db.query(ShoppingListItem).filter(
        ShoppingListItem.shopping_list_id == list_id
    ).delete()
    
    # AGREGAR items optimizados
    for product in result['products']:
        new_item = ShoppingListItem(
            shopping_list_id=list_id,
            product_id=product['id'],
            quantity=1,
            is_substituted=False
        )
        db.add(new_item)
    
    # Actualizar lista
    shopping_list.is_optimized = True
    shopping_list.total_cost = result['metrics']['total_cost']
    shopping_list.total_savings = result['metrics']['savings']
    shopping_list.total_eco_score = result['metrics']['eco_score']
    
    db.commit()
    
    return {
        "message": "List optimized successfully",
        "selected_items": len(result['products']),
        "total_cost": result['metrics']['total_cost'],
        "total_eco_score": result['metrics']['eco_score'],
        "savings": result['metrics']['savings'],
        "optimization_details": {
            "budget_usage": result['metrics']['budget_usage'],
            "total_products": result['metrics']['total_products'],
            "products": result['products']
        }
    }

@router.post("/{list_id}/substitute")
def substitute_products(
    list_id: int,
    aggressive: bool = False,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    shopping_list = db.query(ShoppingList).filter(
        ShoppingList.id == list_id,
        ShoppingList.owner_id == current_user.id
    ).first()
    
    if not shopping_list:
        raise HTTPException(status_code=404, detail="Shopping list not found")
    
    # Obtener productos actuales
    current_products = []
    for item in shopping_list.items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        current_products.append({
            'id': product.id,
            'name': product.name,
            'price': product.price,
            'category': product.category,
            'eco_score': product.eco_score,
            'carbon_footprint': product.carbon_footprint,
            'water_usage': product.water_usage,
            'packaging_score': product.packaging_score,
            'social_score': product.social_score
        })
    
    # Obtener productos disponibles
    all_products = db.query(Product).all()
    available_products = [{
        'id': p.id,
        'name': p.name,
        'price': p.price,
        'category': p.category,
        'eco_score': p.eco_score,
        'carbon_footprint': p.carbon_footprint,
        'water_usage': p.water_usage,
        'packaging_score': p.packaging_score,
        'social_score': p.social_score
    } for p in all_products]
    
    # Aplicar sustituciones
    substitution_service = ProductSubstitution()
    result = substitution_service.substitute_list(
        current_products, 
        available_products,
        aggressive=aggressive
    )
    
    # ACTUALIZAR items sustituidos en la base de datos
    total_savings = 0
    total_score_improvement = 0
    
    for substitution in result.get('substitutions', []):
        original_id = substitution['original']['id']
        substitute_id = substitution['substitute']['id']
        
        # Encontrar el item original
        original_item = db.query(ShoppingListItem).filter(
            ShoppingListItem.shopping_list_id == list_id,
            ShoppingListItem.product_id == original_id
        ).first()
        
        if original_item:
            original_quantity = original_item.quantity
            
            # Verificar si el sustituto YA EXISTE en la lista
            existing_substitute = db.query(ShoppingListItem).filter(
                ShoppingListItem.shopping_list_id == list_id,
                ShoppingListItem.product_id == substitute_id
            ).first()
            
            if existing_substitute:
                # Si ya existe, AUMENTAR la cantidad y eliminar el original
                existing_substitute.quantity += original_quantity
                existing_substitute.is_substituted = True
                db.delete(original_item)
            else:
                # Si no existe, reemplazar el producto
                original_item.product_id = substitute_id
                original_item.is_substituted = True
            
            total_savings += substitution['savings']
            total_score_improvement += substitution['score_improvement']
    
    # Actualizar totales de la lista
    shopping_list.total_savings = total_savings
    if result.get('substitutions'):
        shopping_list.total_eco_score += total_score_improvement
    
    db.commit()
    
    return {
        "message": f"{len(result.get('substitutions', []))} products substituted",
        "substitutions": result.get('substitutions', []),
        "total_savings": total_savings,
        "average_score_improvement": total_score_improvement / len(result.get('substitutions', [])) if result.get('substitutions') else 0
    }

@router.delete("/{list_id}")
def delete_shopping_list(
    list_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    shopping_list = db.query(ShoppingList).filter(
        ShoppingList.id == list_id,
        ShoppingList.owner_id == current_user.id
    ).first()
    
    if not shopping_list:
        raise HTTPException(status_code=404, detail="Shopping list not found")
    
    db.delete(shopping_list)
    db.commit()
    
    return {"message": "Shopping list deleted successfully"}

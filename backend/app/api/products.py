from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from pydantic import BaseModel

from app.database import get_db
from app.models.models import Product
from app.api.auth import get_current_user
from app.algorithms.sustainability import calculate_sustainability_score
from app.algorithms.substitution import find_product_substitutes
from app.services.external_api import OpenFoodFactsService, USDAService
from app.config import USDA_API_KEY

router = APIRouter(prefix="/api/products", tags=["products"])

class ProductCreate(BaseModel):
    barcode: Optional[str] = None
    name: str
    brand: Optional[str] = None
    category: str
    price: float
    unit: Optional[str] = "unidad"
    store: Optional[str] = None
    eco_score: float = 50.0
    carbon_footprint: float = 0.0
    water_usage: float = 0.0
    packaging_score: float = 50.0
    social_score: float = 50.0
    calories: Optional[float] = None
    protein: Optional[float] = None
    fat: Optional[float] = None
    carbs: Optional[float] = None
    image_url: Optional[str] = None
    description: Optional[str] = None

class ProductResponse(BaseModel):
    id: int
    barcode: Optional[str]
    name: str
    brand: Optional[str]
    category: str
    price: float
    unit: Optional[str]
    store: Optional[str]
    eco_score: float
    carbon_footprint: float
    water_usage: float
    packaging_score: float
    social_score: float
    calories: Optional[float]
    protein: Optional[float]
    fat: Optional[float]
    carbs: Optional[float]
    image_url: Optional[str]
    description: Optional[str]
    source_api: Optional[str]
    
    class Config:
        from_attributes = True

@router.get("/", response_model=List[ProductResponse])
def get_products(
    skip: int = 0,
    limit: int = 50,
    category: Optional[str] = None,
    search: Optional[str] = None,
    min_eco_score: Optional[float] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Product)
    
    if category:
        query = query.filter(Product.category == category)
    
    if search:
        query = query.filter(Product.name.ilike(f"%{search}%"))
    
    if min_eco_score is not None:
        query = query.filter(Product.eco_score >= min_eco_score)
    
    products = query.offset(skip).limit(limit).all()
    return products

@router.get("/categories")
def get_categories(db: Session = Depends(get_db)):
    categories = db.query(Product.category, func.count(Product.id)).group_by(Product.category).all()
    return [{"name": cat[0], "count": cat[1]} for cat in categories]

@router.get("/{product_id}", response_model=ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.post("/", response_model=ProductResponse)
def create_product(
    product: ProductCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    db_product = Product(**product.dict(), source_api="manual")
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

@router.get("/{product_id}/sustainability")
def get_product_sustainability(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Obtener todos los productos de la categoría
    category_products = db.query(Product).filter(Product.category == product.category).all()
    
    # Convertir a dicts
    product_dict = {
        'id': product.id,
        'name': product.name,
        'price': product.price,
        'category': product.category,
        'eco_score': product.eco_score,
        'carbon_footprint': product.carbon_footprint,
        'water_usage': product.water_usage,
        'packaging_score': product.packaging_score,
        'social_score': product.social_score,
        'store': product.store,
        'brand': product.brand
    }
    
    all_products_dicts = [{
        'id': p.id,
        'name': p.name,
        'price': p.price,
        'category': p.category,
        'eco_score': p.eco_score
    } for p in category_products]
    
    return calculate_sustainability_score(product_dict, all_products_dicts)

@router.get("/{product_id}/substitutes")
def get_product_substitutes(
    product_id: int,
    max_results: int = 5,
    db: Session = Depends(get_db)
):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Obtener productos de la misma categoría
    available = db.query(Product).filter(
        Product.category == product.category,
        Product.id != product.id
    ).all()
    
    # Convertir a dicts
    product_dict = {
        'id': product.id,
        'name': product.name,
        'price': product.price,
        'category': product.category,
        'carbon_footprint': product.carbon_footprint,
        'water_usage': product.water_usage,
        'packaging_score': product.packaging_score,
        'social_score': product.social_score,
        'eco_score': product.eco_score
    }
    
    available_dicts = [{
        'id': p.id,
        'name': p.name,
        'price': p.price,
        'category': p.category,
        'carbon_footprint': p.carbon_footprint,
        'water_usage': p.water_usage,
        'packaging_score': p.packaging_score,
        'social_score': p.social_score,
        'eco_score': p.eco_score
    } for p in available]
    
    return find_product_substitutes(product_dict, available_dicts, max_results)

@router.get("/search/barcode/{barcode}")
async def search_by_barcode(barcode: str, db: Session = Depends(get_db)):
    # Buscar en DB local primero
    product = db.query(Product).filter(Product.barcode == barcode).first()
    if product:
        return {"source": "local", "product": product}
    
    # Buscar en OpenFoodFacts
    service = OpenFoodFactsService()
    product_data = await service.get_product_by_barcode(barcode)
    
    if product_data:
        return {"source": "openfoodfacts", "product": product_data}
    
    raise HTTPException(status_code=404, detail="Product not found")

@router.get("/search/external")
async def search_external(query: str, source: str = "openfoodfacts"):
    if source == "openfoodfacts":
        service = OpenFoodFactsService()
        products = await service.search_products(query)
    elif source == "usda":
        service = USDAService(USDA_API_KEY)
        products = await service.search_foods(query)
    else:
        raise HTTPException(status_code=400, detail="Invalid source")
    
    return {"products": products, "count": len(products)}

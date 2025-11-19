from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base, SessionLocal
from app.api import auth, products, shopping_lists
from app.models.models import Product
import json
import os

# Create database tables
Base.metadata.create_all(bind=engine)

# Auto-load initial data if database is empty
def load_initial_data_if_empty():
    """Carga productos iniciales si la base de datos está vacía"""
    db = SessionLocal()
    try:
        # Verificar si hay productos
        count = db.query(Product).count()
        if count > 0:
            print(f"Base de datos ya contiene {count} productos")
            return
        
        print("Base de datos vacía, cargando productos iniciales...")
        
        # Buscar archivo JSON
        possible_paths = [
            '/app/products_chile.json',  # Docker
            os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'products_chile.json'),
            'data/products_chile.json',
            '../data/products_chile.json'
        ]
        
        json_path = None
        for path in possible_paths:
            if os.path.exists(path):
                json_path = path
                break
        
        if not json_path:
            print("ADVERTENCIA: No se encontró products_chile.json, base de datos quedará vacía")
            return
        
        # Cargar y insertar productos
        with open(json_path, 'r', encoding='utf-8') as f:
            products_data = json.load(f)
        
        for prod in products_data:
            product = Product(
                barcode=prod.get('barcode'),
                name=prod['name'],
                brand=prod.get('brand'),
                category=prod['category'],
                price=prod['price'],
                unit=prod.get('unit'),
                store=prod.get('store'),
                eco_score=prod.get('eco_score', 50.0),
                carbon_footprint=prod.get('carbon_footprint', 0.0),
                water_usage=prod.get('water_usage', 0.0),
                packaging_score=prod.get('packaging_score', 50.0),
                social_score=prod.get('social_score', 50.0),
                calories=prod.get('calories'),
                protein=prod.get('protein'),
                fat=prod.get('fat'),
                carbs=prod.get('carbs'),
                image_url=prod.get('image_url'),
                description=prod.get('description'),
                source_api='manual'
            )
            db.add(product)
        
        db.commit()
        print(f"Se cargaron {len(products_data)} productos exitosamente!")
        
    except Exception as e:
        print(f"ERROR: Error cargando productos iniciales: {e}")
        db.rollback()
    finally:
        db.close()

# Ejecutar al iniciar la aplicación
load_initial_data_if_empty()

app = FastAPI(
    title="LiquiVerde API",
    description="API para plataforma de retail inteligente y compras sostenibles",
    version="1.0.0"
)

# CORS - Configurar orígenes permitidos desde variable de entorno
allowed_origins = os.getenv(
    "ALLOWED_ORIGINS"
).split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(products.router)
app.include_router(shopping_lists.router)

@app.get("/")
def root():
    return {
        "message": "LiquiVerde API - Grupo Lagos",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}

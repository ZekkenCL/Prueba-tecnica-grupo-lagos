"""
Script para cargar productos iniciales desde JSON a la base de datos
"""

import sys
import os
import json

# Agregar el directorio padre al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal, engine
from app.models.models import Base, Product

# Crear tablas
Base.metadata.create_all(bind=engine)

def load_products():
    db = SessionLocal()
    
    try:
        # Verificar si ya hay productos
        count = db.query(Product).count()
        if count > 0:
            print(f"Ya existen {count} productos en la base de datos. Saltando carga inicial.")
            return
        
        # Leer JSON (buscar en múltiples ubicaciones)
        possible_paths = [
            '/app/products_chile.json',  # Ruta en Docker
            os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'products_chile.json'),  # Ruta relativa
            'data/products_chile.json'  # Ruta directa
        ]
        
        json_path = None
        for path in possible_paths:
            if os.path.exists(path):
                json_path = path
                break
        
        if not json_path:
            raise FileNotFoundError("No se encontró products_chile.json en ninguna ubicación conocida")
        
        with open(json_path, 'r', encoding='utf-8') as f:
            products_data = json.load(f)
        
        # Insertar productos
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
        print(f" Se cargaron {len(products_data)} productos exitosamente!")
        
    except Exception as e:
        print(f" Error cargando productos: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    load_products()

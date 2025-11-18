"""Script para actualizar las URLs de imágenes de productos"""
import json
import os
import sys
sys.path.insert(0, os.path.dirname(__file__))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base
from app.models import Product

# Configuración de base de datos
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@db:5432/liquiverde")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

def update_product_images():
    # Leer el archivo JSON con las imágenes actualizadas
    json_path = '/app/products_chile.json'
    
    with open(json_path, 'r', encoding='utf-8') as f:
        products_data = json.load(f)
    
    db = SessionLocal()
    
    try:
        updated_count = 0
        for product_data in products_data:
            # Buscar producto por barcode
            product = db.query(Product).filter(Product.barcode == product_data['barcode']).first()
            
            if product:
                # Actualizar solo la URL de imagen
                product.image_url = product_data['image_url']
                updated_count += 1
                print(f"Actualizado: {product.name} - {product.image_url}")
        
        db.commit()
        print(f"\n✅ Se actualizaron {updated_count} productos con nuevas imágenes!")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    update_product_images()

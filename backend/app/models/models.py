from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    shopping_lists = relationship("ShoppingList", back_populates="owner", cascade="all, delete-orphan")

class Product(Base):
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True)
    barcode = Column(String, unique=True, index=True)
    name = Column(String, nullable=False, index=True)
    brand = Column(String)
    category = Column(String, index=True)
    price = Column(Float, nullable=False)
    unit = Column(String)  # kg, litros, unidades
    store = Column(String)
    
    # Sostenibilidad
    eco_score = Column(Float, default=0.0)  # 0-100
    carbon_footprint = Column(Float, default=0.0)  # kg CO2
    water_usage = Column(Float, default=0.0)  # litros
    packaging_score = Column(Float, default=0.0)  # 0-100
    social_score = Column(Float, default=0.0)  # 0-100
    
    # Nutricional
    calories = Column(Float)
    protein = Column(Float)
    fat = Column(Float)
    carbs = Column(Float)
    
    # Metadata
    image_url = Column(String)
    description = Column(Text)
    source_api = Column(String)  # openfoodfacts, usda, manual
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class ShoppingList(Base):
    __tablename__ = "shopping_lists"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    budget = Column(Float)  # Presupuesto máximo
    is_optimized = Column(Boolean, default=False)
    total_cost = Column(Float, default=0.0)
    total_savings = Column(Float, default=0.0)
    total_eco_score = Column(Float, default=0.0)
    total_carbon = Column(Float, default=0.0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    owner = relationship("User", back_populates="shopping_lists")
    items = relationship("ShoppingListItem", back_populates="shopping_list", cascade="all, delete-orphan")

class ShoppingListItem(Base):
    __tablename__ = "shopping_list_items"
    
    id = Column(Integer, primary_key=True, index=True)
    shopping_list_id = Column(Integer, ForeignKey("shopping_lists.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, nullable=False, default=1)
    is_substituted = Column(Boolean, default=False)
    original_product_id = Column(Integer, ForeignKey("products.id"))
    
    shopping_list = relationship("ShoppingList", back_populates="items")
    product = relationship("Product", foreign_keys=[product_id])
    original_product = relationship("Product", foreign_keys=[original_product_id])

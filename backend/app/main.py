from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.api import auth, products, shopping_lists

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="LiquiVerde API",
    description="API para plataforma de retail inteligente y compras sostenibles",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
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

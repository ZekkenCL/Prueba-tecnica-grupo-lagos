"""
Servicio para integración con APIs externas de productos
"""

import httpx
from typing import Dict, Optional, List
import json

class OpenFoodFactsService:
    BASE_URL = "https://world.openfoodfacts.org"
    
    async def get_product_by_barcode(self, barcode: str) -> Optional[Dict]:
        """
        Obtiene producto de Open Food Facts por código de barras
        """
        async with httpx.AsyncClient(timeout=10.0) as client:
            try:
                response = await client.get(f"{self.BASE_URL}/api/v0/product/{barcode}.json")
                if response.status_code == 200:
                    data = response.json()
                    if data.get('status') == 1:
                        return self._parse_product(data['product'])
            except Exception as e:
                print(f"Error fetching from OpenFoodFacts: {e}")
        return None
    
    async def search_products(self, query: str, country: str = "chile", page: int = 1) -> List[Dict]:
        """
        Busca productos en Open Food Facts
        """
        async with httpx.AsyncClient(timeout=10.0) as client:
            try:
                params = {
                    'search_terms': query,
                    'page': page,
                    'page_size': 20,
                    'json': 1
                }
                response = await client.get(f"{self.BASE_URL}/cgi/search.pl", params=params)
                if response.status_code == 200:
                    data = response.json()
                    products = []
                    for product in data.get('products', []):
                        parsed = self._parse_product(product)
                        if parsed:
                            products.append(parsed)
                    return products
            except Exception as e:
                print(f"Error searching OpenFoodFacts: {e}")
        return []
    
    def _parse_product(self, product: Dict) -> Optional[Dict]:
        """
        Parsea respuesta de OpenFoodFacts a nuestro formato
        """
        try:
            # Extraer información nutricional
            nutriments = product.get('nutriments', {})
            
            # Calcular eco score (basado en Nutri-Score y Eco-Score si está disponible)
            eco_score = 50.0  # Default
            if 'ecoscore_score' in product:
                eco_score = float(product['ecoscore_score'])
            elif 'nutrition_grade_fr' in product:
                grade_map = {'a': 90, 'b': 75, 'c': 60, 'd': 40, 'e': 20}
                eco_score = grade_map.get(product['nutrition_grade_fr'].lower(), 50)
            
            return {
                'barcode': product.get('code'),
                'name': product.get('product_name', 'Producto desconocido'),
                'brand': product.get('brands', ''),
                'category': product.get('categories', '').split(',')[0] if product.get('categories') else 'General',
                'price': 0.0,  # OpenFoodFacts no tiene precios
                'unit': product.get('quantity', 'unidad'),
                'eco_score': eco_score,
                'carbon_footprint': float(product.get('carbon_footprint_from_known_ingredients_100g', 0)),
                'packaging_score': 50.0,  # Estimar
                'social_score': 50.0,  # Estimar
                'calories': float(nutriments.get('energy-kcal_100g', 0)),
                'protein': float(nutriments.get('proteins_100g', 0)),
                'fat': float(nutriments.get('fat_100g', 0)),
                'carbs': float(nutriments.get('carbohydrates_100g', 0)),
                'image_url': product.get('image_url', ''),
                'source_api': 'openfoodfacts'
            }
        except Exception as e:
            print(f"Error parsing product: {e}")
            return None

class USDAService:
    BASE_URL = "https://api.nal.usda.gov/fdc/v1"
    
    def __init__(self, api_key: str = "DEMO_KEY"):
        self.api_key = api_key
    
    async def search_foods(self, query: str) -> List[Dict]:
        """
        Busca alimentos en USDA FoodData Central
        """
        async with httpx.AsyncClient(timeout=10.0) as client:
            try:
                params = {
                    'api_key': self.api_key,
                    'query': query,
                    'pageSize': 20
                }
                response = await client.get(f"{self.BASE_URL}/foods/search", params=params)
                if response.status_code == 200:
                    data = response.json()
                    products = []
                    for food in data.get('foods', []):
                        parsed = self._parse_food(food)
                        if parsed:
                            products.append(parsed)
                    return products
            except Exception as e:
                print(f"Error searching USDA: {e}")
        return []
    
    def _parse_food(self, food: Dict) -> Optional[Dict]:
        """
        Parsea respuesta de USDA a nuestro formato
        """
        try:
            # Extraer nutrientes
            nutrients = {n['nutrientName'].lower(): n.get('value', 0) 
                        for n in food.get('foodNutrients', [])}
            
            return {
                'barcode': None,
                'name': food.get('description', 'Alimento'),
                'brand': food.get('brandOwner', ''),
                'category': food.get('foodCategory', 'General'),
                'price': 0.0,
                'unit': '100g',
                'eco_score': 50.0,
                'carbon_footprint': 0.0,
                'packaging_score': 50.0,
                'social_score': 50.0,
                'calories': float(nutrients.get('energy', 0)),
                'protein': float(nutrients.get('protein', 0)),
                'fat': float(nutrients.get('total lipid (fat)', 0)),
                'carbs': float(nutrients.get('carbohydrate, by difference', 0)),
                'image_url': '',
                'source_api': 'usda'
            }
        except Exception as e:
            print(f"Error parsing food: {e}")
            return None

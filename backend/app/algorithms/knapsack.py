"""
Algoritmo de Mochila Multi-objetivo (Multi-objective Knapsack Problem)
Para optimización de listas de compras considerando:
- Costo total (minimizar)
- Sostenibilidad (maximizar)
- Valor nutricional (maximizar)
"""

from typing import List, Dict, Tuple
import random

class Product:
    def __init__(self, id: int, name: str, price: float, eco_score: float, 
                 nutrition_score: float, quantity: int = 1, category: str = ''):
        self.id = id
        self.name = name
        self.price = price
        self.eco_score = eco_score
        self.nutrition_score = nutrition_score
        self.quantity = quantity
        self.category = category
    
    def total_price(self):
        return self.price * self.quantity
    
    def total_eco_score(self):
        return self.eco_score * self.quantity
    
    def total_nutrition(self):
        return self.nutrition_score * self.quantity

class MultiObjectiveKnapsack:
    def __init__(self, budget: float, eco_weight: float = 0.3, 
                 nutrition_weight: float = 0.2, price_weight: float = 0.5):
        self.budget = budget
        self.eco_weight = eco_weight
        self.nutrition_weight = nutrition_weight
        self.price_weight = price_weight
    
    def fitness(self, products: List[Product]) -> float:
        """
        Calcula el fitness de una solución considerando múltiples objetivos
        """
        total_price = sum(p.total_price() for p in products)
        
        # Si excede el presupuesto, penalizar fuertemente
        if total_price > self.budget:
            return -1000.0
        
        total_eco = sum(p.total_eco_score() for p in products)
        total_nutrition = sum(p.total_nutrition() for p in products)
        
        # Normalizar valores
        price_score = (self.budget - total_price) / self.budget  # Mientras menos gastemos, mejor
        eco_score = total_eco / 100.0 if len(products) > 0 else 0
        nutrition_score = total_nutrition / 100.0 if len(products) > 0 else 0
        
        # Fitness ponderado
        fitness = (
            self.price_weight * price_score +
            self.eco_weight * eco_score +
            self.nutrition_weight * nutrition_score
        )
        
        return fitness
    
    def optimize(self, available_products: List[Product], 
                 required_products: List[Product] = None,
                 iterations: int = 1000) -> Tuple[List[Product], Dict]:
        """
        Algoritmo genético para optimizar la lista de compras
        """
        if not available_products:
            return [], {"total_cost": 0, "eco_score": 0, "savings": 0}
        
        # Inicializar productos requeridos
        if required_products is None:
            required_products = []
        
        # LIMPIAR productos requeridos: mantener solo el mejor de cada categoría
        cleaned_required = []
        category_best = {}
        
        for p in required_products:
            category = p.category if p.category else ''
            if category:
                if category not in category_best or p.eco_score > category_best[category].eco_score:
                    category_best[category] = p
            else:
                cleaned_required.append(p)
        
        # Agregar los mejores de cada categoría
        cleaned_required.extend(category_best.values())
        required_products = cleaned_required
        
        best_solution = required_products.copy()
        best_fitness = self.fitness(best_solution)
        
        # Algoritmo genético simple
        for _ in range(iterations):
            # Crear solución candidata
            candidate = required_products.copy()
            
            # Obtener categorías de productos requeridos para evitar duplicados de menor calidad
            required_categories = {}
            for p in required_products:
                category = p.category if p.category else ''
                if category and (category not in required_categories or p.eco_score > required_categories[category]):
                    required_categories[category] = p.eco_score
            
            # Agregar productos aleatorios que no excedan presupuesto
            available = [p for p in available_products if p not in candidate]
            random.shuffle(available)
            
            for product in available:
                # Evitar agregar productos de la misma categoría con peor eco-score
                product_category = product.category if product.category else ''
                if product_category and product_category in required_categories:
                    if product.eco_score <= required_categories[product_category]:
                        continue  # Skip productos peores de la misma categoría
                
                temp_solution = candidate + [product]
                total_cost = sum(p.total_price() for p in temp_solution)
                
                if total_cost <= self.budget:
                    candidate.append(product)
                    # Actualizar la mejor opción de esta categoría
                    if product_category and (product_category not in required_categories or product.eco_score > required_categories[product_category]):
                        required_categories[product_category] = product.eco_score
            
            # Evaluar fitness
            candidate_fitness = self.fitness(candidate)
            
            # Actualizar mejor solución
            if candidate_fitness > best_fitness:
                best_solution = candidate
                best_fitness = candidate_fitness
        
        # Calcular métricas finales
        total_cost = sum(p.total_price() for p in best_solution)
        total_eco = sum(p.total_eco_score() for p in best_solution)
        savings = self.budget - total_cost
        
        metrics = {
            "total_cost": round(total_cost, 2),
            "eco_score": round(total_eco / len(best_solution) if best_solution else 0, 2),
            "savings": round(savings, 2),
            "total_products": len(best_solution),
            "budget_usage": round((total_cost / self.budget) * 100, 2)
        }
        
        return best_solution, metrics

def optimize_shopping_list(products: List[Dict], budget: float, 
                          required_product_ids: List[int] = None) -> Dict:
    """
    Función helper para optimizar lista de compras
    """
    # Convertir diccionarios a objetos Product
    product_objects = []
    for p in products:
        # Calcular score nutricional simple
        nutrition_score = (
            (p.get('protein', 0) * 0.4) +
            (p.get('calories', 0) / 20) -
            (p.get('fat', 0) * 0.3)
        )
        nutrition_score = max(0, min(100, nutrition_score))
        
        product_objects.append(
            Product(
                id=p['id'],
                name=p['name'],
                price=p['price'],
                eco_score=p.get('eco_score', 50.0),
                nutrition_score=nutrition_score,
                quantity=p.get('quantity', 1),
                category=p.get('category', '')
            )
        )
    
    # Separar productos requeridos
    required = []
    available = []
    
    if required_product_ids:
        for p in product_objects:
            if p.id in required_product_ids:
                required.append(p)
            else:
                available.append(p)
    else:
        available = product_objects
    
    # Optimizar
    optimizer = MultiObjectiveKnapsack(budget)
    optimized_products, metrics = optimizer.optimize(available, required)
    
    # Convertir de vuelta a diccionarios
    result_products = []
    for p in optimized_products:
        original = next((prod for prod in products if prod['id'] == p.id), None)
        if original:
            result_products.append(original)
    
    return {
        "products": result_products,
        "metrics": metrics
    }

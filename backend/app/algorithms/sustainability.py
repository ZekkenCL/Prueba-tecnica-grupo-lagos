"""
Sistema de Scoring de Sostenibilidad
Calcula puntuación considerando factores:
- Económico (precio vs promedio)
- Ambiental (huella de carbono, agua, empaque)
- Social (condiciones laborales, comercio justo)
"""

from typing import Dict

class SustainabilityScorer:
    def __init__(self):
        self.weights = {
            'economic': 0.35,
            'environmental': 0.40,
            'social': 0.25
        }
    
    def calculate_economic_score(self, product: Dict, category_avg_price: float = None) -> float:
        """
        Score económico: productos más baratos tienen mejor score
        """
        price = product.get('price', 0)
        
        if category_avg_price and category_avg_price > 0:
            # Comparar con promedio de categoría
            ratio = price / category_avg_price
            if ratio <= 0.8:  # 20% más barato
                return 100
            elif ratio <= 1.0:  # Hasta el promedio
                return 80 + (1.0 - ratio) * 100
            elif ratio <= 1.2:  # Hasta 20% más caro
                return 60 - ((ratio - 1.0) * 100)
            else:  # Más de 20% más caro
                return max(0, 40 - ((ratio - 1.2) * 50))
        else:
            # Score basado en precio absoluto
            if price <= 1000:
                return 100
            elif price <= 3000:
                return 80
            elif price <= 5000:
                return 60
            else:
                return 40
    
    def calculate_environmental_score(self, product: Dict) -> float:
        """
        Score ambiental: huella de carbono, agua, empaque
        """
        carbon = product.get('carbon_footprint', 0)
        water = product.get('water_usage', 0)
        packaging = product.get('packaging_score', 50)
        
        # Carbon score (menor es mejor)
        if carbon <= 0.5:
            carbon_score = 100
        elif carbon <= 1.0:
            carbon_score = 80
        elif carbon <= 2.0:
            carbon_score = 60
        elif carbon <= 5.0:
            carbon_score = 40
        else:
            carbon_score = 20
        
        # Water score (menor es mejor)
        if water <= 10:
            water_score = 100
        elif water <= 50:
            water_score = 80
        elif water <= 100:
            water_score = 60
        elif water <= 200:
            water_score = 40
        else:
            water_score = 20
        
        # Packaging score (ya normalizado 0-100)
        packaging_score = packaging
        
        # Promedio ponderado
        env_score = (
            carbon_score * 0.4 +
            water_score * 0.3 +
            packaging_score * 0.3
        )
        
        return round(env_score, 2)
    
    def calculate_social_score(self, product: Dict) -> float:
        """
        Score social: condiciones laborales, comercio justo, origen
        """
        social_score = product.get('social_score', 50)
        
        # Ajustar por origen (productos locales tienen mejor score)
        store = product.get('store', '').lower()
        if 'local' in store or 'feria' in store:
            social_score = min(100, social_score + 15)
        
        # Ajustar por certificaciones
        brand = product.get('brand', '').lower()
        if 'organico' in brand or 'comercio justo' in brand:
            social_score = min(100, social_score + 10)
        
        return round(social_score, 2)
    
    def calculate_total_score(self, product: Dict, category_avg_price: float = None) -> Dict:
        """
        Calcula el score total de sostenibilidad
        """
        economic = self.calculate_economic_score(product, category_avg_price)
        environmental = self.calculate_environmental_score(product)
        social = self.calculate_social_score(product)
        
        total = (
            economic * self.weights['economic'] +
            environmental * self.weights['environmental'] +
            social * self.weights['social']
        )
        
        return {
            'total_score': round(total, 2),
            'economic_score': round(economic, 2),
            'environmental_score': round(environmental, 2),
            'social_score': round(social, 2),
            'breakdown': {
                'carbon_footprint': product.get('carbon_footprint', 0),
                'water_usage': product.get('water_usage', 0),
                'packaging_score': product.get('packaging_score', 50)
            }
        }
    
    def compare_products(self, product1: Dict, product2: Dict) -> Dict:
        """
        Compara dos productos y determina cuál es más sostenible
        """
        score1 = self.calculate_total_score(product1)
        score2 = self.calculate_total_score(product2)
        
        diff = score1['total_score'] - score2['total_score']
        
        return {
            'product1_score': score1,
            'product2_score': score2,
            'difference': round(diff, 2),
            'better_product': 1 if diff > 0 else 2,
            'improvement_percentage': round(abs(diff), 2)
        }

def calculate_sustainability_score(product: Dict, category_avg_price: float = None) -> Dict:
    """
    Función helper para calcular score de sostenibilidad
    """
    scorer = SustainabilityScorer()
    return scorer.calculate_total_score(product, category_avg_price)

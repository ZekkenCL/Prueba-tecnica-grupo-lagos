"""
Algoritmo de Sustitución Inteligente de Productos
Encuentra alternativas más sostenibles y económicas
"""

from typing import List, Dict, Optional
from app.algorithms.sustainability import SustainabilityScorer

class ProductSubstitution:
    def __init__(self):
        self.scorer = SustainabilityScorer()
    
    def find_substitutes(self, original_product: Dict, available_products: List[Dict],
                        max_price_increase: float = 0.2, min_score_improvement: float = 1.0,
                        max_results: int = 5) -> List[Dict]:
        """
        Encuentra productos sustitutos basándose en:
        - Misma categoría
        - Precio similar o menor
        - Mayor eco-score (puntuación ambiental)
        """
        if not available_products:
            return []
        
        original_category = original_product.get('category', '')
        original_price = original_product.get('price', 0)
        original_eco_score = original_product.get('eco_score', 0)
        
        max_price = original_price * (1 + max_price_increase)
        
        candidates = []
        
        for product in available_products:
            # Evitar el producto original
            if product.get('id') == original_product.get('id'):
                continue
            
            # Filtrar por categoría
            if product.get('category') != original_category:
                continue
            
            # Filtrar por precio
            product_price = product.get('price', 0)
            if product_price > max_price:
                continue
            
            # Usar eco_score directamente
            product_eco_score = product.get('eco_score', 0)
            
            # Verificar que sea MÁS sostenible (eco_score mayor)
            score_improvement = product_eco_score - original_eco_score
            if score_improvement < min_score_improvement:
                continue
            
            # Calcular ahorro/costo adicional
            price_diff = product_price - original_price
            savings_percentage = ((original_price - product_price) / original_price) * 100
            
            candidates.append({
                'product': product,
                'score': product_eco_score,
                'score_improvement': round(score_improvement, 2),
                'price_difference': round(price_diff, 2),
                'savings_percentage': round(savings_percentage, 2),
                'recommendation_reason': self._generate_reason(
                    score_improvement, price_diff, product_eco_score
                )
            })
        
        # Ordenar por score improvement (descendente)
        candidates.sort(key=lambda x: x['score_improvement'], reverse=True)
        
        return candidates[:max_results]
    
    def _generate_reason(self, score_improvement: float, price_diff: float, 
                        eco_score: float) -> str:
        """
        Genera una razón legible para la recomendación
        """
        reasons = []
        
        if score_improvement >= 20:
            reasons.append("Mucho más sostenible")
        elif score_improvement >= 10:
            reasons.append("Más sostenible")
        else:
            reasons.append("Levemente más sostenible")
        
        if price_diff < -500:
            reasons.append(f"Ahorras ${abs(price_diff):.0f}")
        elif price_diff < 0:
            reasons.append("Más económico")
        elif price_diff == 0:
            reasons.append("Mismo precio")
        else:
            reasons.append(f"${price_diff:.0f} más caro")
        
        # Destacar eco-score alto
        if eco_score >= 80:
            reasons.append("Excelente eco-score")
        
        return " • ".join(reasons)
    
    def substitute_list(self, shopping_list: List[Dict], available_products: List[Dict],
                       aggressive: bool = False) -> Dict:
        """
        Aplica sustituciones a toda la lista de compras
        aggressive: True = sustituye aunque sea más caro si es mucho más sostenible
        """
        max_price_increase = 0.5 if aggressive else 0.35
        min_score_improvement = 1.0 if aggressive else 2.0
        
        substitutions = []
        total_savings = 0
        total_score_improvement = 0
        
        for item in shopping_list:
            substitutes = self.find_substitutes(
                item, 
                available_products,
                max_price_increase=max_price_increase,
                min_score_improvement=min_score_improvement,
                max_results=1
            )
            
            if substitutes:
                best_substitute = substitutes[0]
                substitutions.append({
                    'original': item,
                    'substitute': best_substitute['product'],
                    'reason': best_substitute['recommendation_reason'],
                    'savings': best_substitute['price_difference'],
                    'score_improvement': best_substitute['score_improvement']
                })
                
                total_savings += best_substitute['price_difference']
                total_score_improvement += best_substitute['score_improvement']
        
        return {
            'substitutions': substitutions,
            'total_substitutions': len(substitutions),
            'total_savings': round(total_savings, 2),
            'average_score_improvement': round(
                total_score_improvement / len(substitutions) if substitutions else 0, 2
            )
        }

def find_product_substitutes(product: Dict, available_products: List[Dict], 
                            max_results: int = 5) -> List[Dict]:
    """
    Función helper para encontrar sustitutos
    """
    substitution = ProductSubstitution()
    return substitution.find_substitutes(product, available_products, max_results=max_results)

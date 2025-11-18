# LiquiVerde - Plataforma de Retail Inteligente

## 📋 Descripción

LiquiVerde es una plataforma web de retail inteligente que ayuda a los consumidores a ahorrar dinero mientras toman decisiones de compra sostenibles. La aplicación permite a los usuarios crear listas de compras optimizadas, analizar la sostenibilidad de productos y encontrar alternativas más económicas y ecológicas.

## ✨ Características Principales

- **Gestión de Productos**: Catálogo de 20 productos chilenos con información nutricional y de sostenibilidad
- **Optimización de Listas**: Algoritmo de Knapsack multi-objetivo para maximizar valor dentro del presupuesto
- **Análisis de Sostenibilidad**: Sistema de scoring que evalúa impacto económico, ambiental y social
- **Sustitución Inteligente**: Recomendaciones de productos alternativos más sostenibles
- **Autenticación**: Sistema de registro y login con JWT
- **Interfaz Moderna**: React con diseño responsive y temática sostenible

## 🚀 Instrucciones para Ejecutar Localmente

### Prerrequisitos

- Docker Desktop instalado y en ejecución
- Git para clonar el repositorio
- (Opcional) Node.js 18+ y Python 3.11+ para desarrollo sin Docker

### Opción 1: Ejecutar con Docker (Recomendado)

1. **Clonar el repositorio**
```bash
git clone <url-del-repositorio>
cd "Prueba tecnica grupo lagos"
```

2. **Configurar variables de entorno**

El proyecto ya incluye archivos `.env` configurados, pero puedes personalizarlos si lo deseas:

**Backend** (`backend/.env`):
```env
DATABASE_URL=postgresql://liquiverde:liquiverde123@db:5432/liquiverde
REDIS_URL=redis://redis:6379/0
SECRET_KEY=your-secret-key-here-change-in-production-123456789
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
USDA_API_KEY=  # Opcional: tu API key de USDA FoodData Central
```

**Frontend** (`frontend/.env`):
```env
VITE_API_URL=http://localhost:8000/api
```

3. **Iniciar todos los servicios con Docker Compose**
```bash
docker-compose up --build
```

Este comando:
- Construye las imágenes de Docker para backend y frontend
- Inicia PostgreSQL en el puerto 5432
- Inicia Redis en el puerto 6379
- Inicia el backend FastAPI en http://localhost:8000
- Inicia el frontend React en http://localhost:5173

4. **Cargar datos iniciales** (en otra terminal mientras los contenedores están corriendo)
```bash
docker-compose exec backend python app/load_initial_data.py
```

5. **Acceder a la aplicación**
- Frontend: http://localhost:5173
- API Backend: http://localhost:8000
- Documentación API: http://localhost:8000/docs

6. **Detener los servicios**
```bash
docker-compose down
```

Para eliminar también los volúmenes (base de datos):
```bash
docker-compose down -v
```

### Opción 2: Ejecutar sin Docker (Desarrollo)

#### Backend

1. **Instalar PostgreSQL y Redis localmente**

2. **Configurar entorno virtual de Python**
```bash
cd backend
python -m venv venv
venv\Scripts\activate  # En Windows
pip install -r requirements.txt
```

3. **Configurar variables de entorno**
Editar `backend/.env` con las URLs locales:
```env
DATABASE_URL=postgresql://usuario:password@localhost:5432/liquiverde
REDIS_URL=redis://localhost:6379/0
```

4. **Iniciar el backend**
```bash
uvicorn app.main:app --reload
```

#### Frontend

1. **Instalar dependencias**
```bash
cd frontend
npm install
```

2. **Iniciar servidor de desarrollo**
```bash
npm run dev
```

La aplicación estará disponible en http://localhost:5173

## 📊 Explicación de Algoritmos Implementados

### 1. Algoritmo de Knapsack Multi-Objetivo

**Ubicación**: `backend/app/algorithms/knapsack.py`

**Propósito**: Optimizar listas de compras maximizando valor nutricional y sostenibilidad dentro de un presupuesto limitado.

**Funcionamiento**:

El algoritmo utiliza un enfoque de algoritmo genético para resolver el problema de la mochila (knapsack) con múltiples objetivos:

```
Función Objetivo = w1 * eco_score + w2 * nutrition_score - penalización_presupuesto

Donde:
- w1 = 0.6 (peso del score ecológico)
- w2 = 0.4 (peso del score nutricional)
- eco_score = Puntuación de sostenibilidad del producto (0-100)
- nutrition_score = (proteínas * 4 + carbohidratos * 4 + grasas * 9) / 10
- penalización_presupuesto = 1000 si costo_total > presupuesto, sino 0
```

**Proceso**:
1. Se genera una población inicial de soluciones aleatorias
2. Se evalúa el fitness de cada solución según la fórmula
3. Se itera 1000 veces aplicando mutaciones aleatorias
4. Se mantiene la mejor solución encontrada
5. Se retorna la lista optimizada con métricas calculadas

**Complejidad**: O(n * iteraciones) donde n es el número de productos

**Ejemplo de Uso**:
```python
knapsack = MultiObjectiveKnapsack(products, budget=10000)
result = knapsack.optimize()
# result = {
#   "products": [...],
#   "total_cost": 8500,
#   "total_eco_score": 82.5,
#   "total_savings": 1500,
#   "budget_usage": 85.0
# }
```

### 2. Sistema de Scoring de Sostenibilidad

**Ubicación**: `backend/app/algorithms/sustainability.py`

**Propósito**: Evaluar productos en tres dimensiones de sostenibilidad y generar una puntuación general.

**Funcionamiento**:

El sistema calcula tres scores independientes que luego combina:

**Score Económico (35% del total)**:
```
score_economico = max(0, 100 - ((precio - precio_promedio_categoria) / precio_promedio_categoria * 100))
```
- Compara el precio con el promedio de su categoría
- Productos más baratos obtienen mayor puntuación

**Score Ambiental (40% del total)**:
```
componente_carbono = (1 - min(carbon_footprint / 5.0, 1)) * 40
componente_agua = (1 - min(water_usage / 1000, 1)) * 35
componente_empaque = packaging_score * 0.25

score_ambiental = componente_carbono + componente_agua + componente_empaque
```
- Evalúa huella de carbono (kg CO₂)
- Analiza uso de agua (litros)
- Considera calidad del empaque (reciclabilidad)

**Score Social (25% del total)**:
```
score_social = social_score directamente del producto
```
- Considera comercio justo
- Evalúa condiciones laborales
- Analiza impacto en comunidad local

**Score General**:
```
score_general = (score_economico * 0.35) + (score_ambiental * 0.40) + (score_social * 0.25)
```

**Ejemplo de Uso**:
```python
scorer = SustainabilityScorer()
analysis = scorer.calculate_score(product)
# analysis = {
#   "overall_score": 78.5,
#   "economic_score": 82.0,
#   "environmental_score": 76.0,
#   "social_score": 80.0,
#   "category": "Lácteos"
# }
```

### 3. Algoritmo de Sustitución Inteligente de Productos

**Ubicación**: `backend/app/algorithms/substitution.py`

**Propósito**: Encontrar alternativas más sostenibles para productos en una lista de compras.

**Funcionamiento**:

El algoritmo busca sustitutos que cumplan con criterios estrictos:

**Criterios de Sustitución**:
1. **Misma Categoría**: El sustituto debe pertenecer a la misma categoría (ej: Lácteos)
2. **Precio Similar o Menor**: `precio_sustituto <= precio_original * (1 + max_price_increase)`
3. **Mejor Sostenibilidad**: `eco_score_sustituto > eco_score_original + min_score_improvement`

**Parámetros Configurables**:
- `max_price_increase`: 10% (permite hasta 10% más caro)
- `min_score_improvement`: 5.0 puntos (mejora mínima requerida)

**Proceso**:
```python
def find_substitutes(product, all_products):
    candidatos = filtrar_por_categoria(product.category)
    candidatos = filtrar_por_precio(precio <= original * 1.10)
    candidatos = filtrar_por_eco_score(score > original + 5.0)
    return ordenar_por_eco_score_descendente(candidatos)[:3]
```

**Aplicación a Lista Completa**:
```python
def substitute_list(shopping_list):
    for item in shopping_list.items:
        substitutos = find_substitutes(item.product)
        if substitutos:
            mejor_sustituto = substitutos[0]
            item.product = mejor_sustituto
            item.is_substituted = True
            item.original_product_id = producto_original.id
```

**Ejemplo de Uso**:
```python
substitution = ProductSubstitution()
alternatives = substitution.find_substitutes(
    product=colun_milk,
    all_products=product_catalog,
    max_price_increase=0.10,
    min_score_improvement=5.0
)
# alternatives = [
#   {"id": 15, "name": "Soprole Leche Descremada", "eco_score": 78, "price": 950},
#   ...
# ]
```

## 🗃️ Estructura del Proyecto

```
Prueba tecnica grupo lagos/
├── backend/
│   ├── app/
│   │   ├── algorithms/
│   │   │   ├── knapsack.py          # Algoritmo de optimización
│   │   │   ├── sustainability.py    # Sistema de scoring
│   │   │   └── substitution.py      # Sustitución inteligente
│   │   ├── api/
│   │   │   ├── auth.py              # Endpoints de autenticación
│   │   │   ├── products.py          # CRUD de productos
│   │   │   └── shopping_lists.py    # Gestión de listas
│   │   ├── models/
│   │   │   └── models.py            # Modelos SQLAlchemy
│   │   ├── services/
│   │   │   └── external_api.py      # APIs externas
│   │   ├── load_initial_data.py     # Script de carga de datos
│   │   └── main.py                  # Aplicación FastAPI
│   ├── data/
│   │   └── products_chile.json      # Dataset de productos
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Navbar.jsx           # Barra de navegación
│   │   │   └── ProtectedRoute.jsx   # Protección de rutas
│   │   ├── context/
│   │   │   └── AuthContext.jsx      # Contexto de autenticación
│   │   ├── pages/
│   │   │   ├── Home.jsx             # Página de inicio
│   │   │   ├── Login.jsx            # Inicio de sesión
│   │   │   ├── Register.jsx         # Registro de usuario
│   │   │   ├── Products.jsx         # Lista de productos
│   │   │   ├── ProductDetail.jsx    # Detalle de producto
│   │   │   ├── ShoppingLists.jsx    # Listas de compras
│   │   │   └── ShoppingListDetail.jsx
│   │   ├── services/
│   │   │   └── api.js               # Cliente Axios
│   │   ├── App.jsx                  # Componente principal
│   │   └── main.jsx                 # Punto de entrada
│   ├── Dockerfile
│   └── package.json
├── docker-compose.yml
└── README.md
```

## 🔧 Tecnologías Utilizadas

### Backend
- **FastAPI 0.104.1**: Framework web moderno y de alto rendimiento
- **SQLAlchemy 2.0.23**: ORM para interacción con base de datos
- **PostgreSQL 15**: Base de datos relacional
- **Redis 5.0.1**: Caché en memoria
- **Python-Jose 3.3.0**: Manejo de tokens JWT
- **Passlib 1.7.4**: Hash seguro de contraseñas
- **httpx 0.25.2**: Cliente HTTP para APIs externas

### Frontend
- **React 18**: Biblioteca para interfaces de usuario
- **Vite 7.2.2**: Build tool y dev server rápido
- **React Router DOM 6**: Enrutamiento
- **Axios**: Cliente HTTP
- **React Icons**: Iconos

### DevOps
- **Docker & Docker Compose**: Containerización
- **Uvicorn**: Servidor ASGI para FastAPI

## 🔌 APIs Externas Integradas

### OpenFoodFacts API
- **URL**: https://world.openfoodfacts.org/api/v0/
- **Uso**: Búsqueda de productos por código de barras
- **Datos obtenidos**: Información nutricional, ingredientes, Nutri-Score

### USDA FoodData Central API
- **URL**: https://api.nal.usda.gov/fdc/v1/
- **Uso**: Búsqueda de alimentos y nutrientes
- **API Key**: Opcional (configurar en `.env`)
- **Datos obtenidos**: Valores nutricionales detallados

## 📦 Dataset de Productos

El proyecto incluye 20 productos chilenos reales con datos de sostenibilidad:

**Categorías incluidas**:
- Lácteos (Colun, Soprole)
- Panadería (Ideal, Fuchs)
- Abarrotes (Arroz, Fideos, Aceites)
- Carnes (Pollo, Vacuno, Cerdo)
- Verduras y Frutas (productos locales de feria)

**Datos por producto**:
- Información básica: nombre, marca, precio, unidad
- Sostenibilidad: eco_score, carbon_footprint, water_usage, packaging_score
- Nutrición: calorías, proteínas, grasas, carbohidratos
- Código de barras y categoría

## 🤖 Sección: Uso de Inteligencia Artificial

Este proyecto fue desarrollado con asistencia significativa de **GitHub Copilot** (Claude Sonnet 4.5) como herramienta de IA para programación.

### Áreas donde se utilizó IA:

#### 1. **Arquitectura y Diseño** (Alta asistencia)
- Diseño de la estructura del proyecto backend/frontend
- Definición de modelos de base de datos con SQLAlchemy
- Arquitectura de componentes React con Context API
- Configuración de Docker Compose multi-servicio

**Resultado**: La IA proporcionó una estructura profesional y escalable, sugiriendo mejores prácticas de separación de concerns y organización de código.

#### 2. **Implementación de Algoritmos** (Alta asistencia)
- **Algoritmo de Knapsack Multi-objetivo**: La IA ayudó a diseñar la función de fitness considerando múltiples objetivos (sostenibilidad, nutrición, presupuesto) y sugirió el enfoque iterativo con mutaciones aleatorias.
- **Sistema de Scoring de Sostenibilidad**: Asistencia en el diseño de las fórmulas de ponderación (35% económico, 40% ambiental, 25% social) y normalización de valores.
- **Algoritmo de Sustitución**: Ayuda en la lógica de filtrado por categoría, precio y mejora de score.

**Valor agregado humano**: Ajuste de parámetros específicos para el contexto chileno, validación de lógica de negocio y selección de umbrales adecuados (ej: 10% tolerancia en precio, 5 puntos mejora mínima).

#### 3. **Backend FastAPI** (Alta asistencia)
- Generación de endpoints RESTful completos con documentación OpenAPI
- Implementación de autenticación JWT con OAuth2PasswordBearer
- Manejo de dependencias y inyección de base de datos
- Integración con APIs externas (OpenFoodFacts, USDA)

**Decisiones humanas**: Elección de estructura de respuestas, manejo de errores específicos, configuración de CORS para desarrollo.

#### 4. **Frontend React** (Alta asistencia)
- Creación de 7 componentes de página completos con lógica de estado
- Implementación de Context API para autenticación global
- Diseño de interfaz con inline styles y temática sostenible
- Integración con backend vía Axios con interceptores

**Aporte humano**: Decisiones de UX/UI, flujo de navegación, mensajes en español, elección de colores (#27ae60 como verde principal).

#### 5. **Datos y Dataset** (Asistencia Media)
- Generación del archivo `products_chile.json` con 20 productos
- La IA sugirió marcas chilenas reales (Colun, Soprole, Ideal, Tucapel)
- Valores realistas de precios y métricas de sostenibilidad

**Validación humana**: Revisión de precios para asegurar realismo, ajuste de scores de sostenibilidad según conocimiento del mercado local.

#### 6. **Dockerización y DevOps** (Alta asistencia)
- Configuración de `docker-compose.yml` con 4 servicios
- Dockerfiles para backend y frontend
- Configuración de healthchecks y dependencias entre servicios
- Variables de entorno para configuración

#### 7. **Documentación** (Alta asistencia)
- Generación de este README con explicaciones detalladas
- Documentación de algoritmos con fórmulas matemáticas
- Instrucciones de instalación y uso

**Refinamiento humano**: Organización de secciones, énfasis en puntos importantes, ejemplos específicos.

### Limitaciones y Supervisión Humana:

1. **Testing**: El código NO incluye tests automatizados. La validación fue manual.
2. **Optimización**: Los algoritmos priorizan claridad sobre eficiencia (ej: 1000 iteraciones fijas en lugar de convergencia adaptativa).
3. **Seguridad**: SECRET_KEY y configuraciones deben cambiarse para producción.
4. **Manejo de Errores**: Los try-catch son básicos, se necesitaría logging más robusto en producción.
5. **Validaciones**: Validaciones de entrada básicas, no exhaustivas.

### Aprendizajes del Uso de IA:

✅ **Ventajas**:
- Aceleración significativa del desarrollo (proyecto completo en tiempo reducido)
- Código consistente con buenas prácticas
- Documentación detallada automática
- Solución de problemas técnicos rápida

⚠️ **Desafíos**:
- Necesidad de validar lógica de negocio manualmente
- Revisión cuidadosa de valores numéricos y fórmulas
- Decisiones arquitectónicas requieren comprensión profunda

### Transparencia:

Este proyecto **NO** hubiera sido posible en el mismo tiempo sin asistencia de IA. GitHub Copilot fue utilizado como:
- **Copiloto de código**: Generación de estructuras y lógica básica
- **Consultor técnico**: Resolución de dudas sobre frameworks
- **Generador de boilerplate**: Código repetitivo y configuraciones

Sin embargo, **todas las decisiones finales de diseño, arquitectura y lógica de negocio fueron tomadas y validadas por el desarrollador humano**.

## 🔐 Seguridad

- Contraseñas hasheadas con bcrypt
- Tokens JWT con expiración de 30 minutos
- Rutas protegidas en frontend y backend
- Variables sensibles en archivos `.env`
- CORS configurado para localhost en desarrollo

**⚠️ IMPORTANTE**: Cambiar `SECRET_KEY` en producción.

## 📝 Endpoints API Principales

### Autenticación
- `POST /api/auth/register` - Registro de usuario
- `POST /api/auth/login` - Inicio de sesión
- `GET /api/auth/me` - Usuario actual

### Productos
- `GET /api/products/` - Listar productos
- `GET /api/products/{id}` - Detalle de producto
- `GET /api/products/{id}/sustainability` - Análisis de sostenibilidad
- `GET /api/products/{id}/substitutes` - Alternativas sostenibles
- `GET /api/products/search/barcode/{barcode}` - Buscar por código de barras

### Listas de Compras
- `GET /api/shopping-lists/` - Listar mis listas
- `POST /api/shopping-lists/` - Crear lista
- `POST /api/shopping-lists/{id}/items` - Agregar producto a lista
- `POST /api/shopping-lists/{id}/optimize` - Optimizar lista
- `POST /api/shopping-lists/{id}/substitute` - Aplicar sustituciones
- `DELETE /api/shopping-lists/{id}` - Eliminar lista

## 🧪 Pruebas

Para probar la aplicación:

1. Registrar un nuevo usuario en http://localhost:5173/register
2. Iniciar sesión
3. Explorar el catálogo de productos
4. Crear una lista de compras con presupuesto (ej: $15,000)
5. Agregar varios productos a la lista
6. Hacer clic en "Optimizar Lista" para ver el algoritmo de Knapsack en acción
7. Hacer clic en "Buscar Alternativas" para aplicar sustituciones inteligentes
8. Ver el detalle de cualquier producto para análisis de sostenibilidad completo

## 📄 Licencia

Este proyecto fue desarrollado como prueba técnica para Grupo Lagos.

## 👤 Autor

Desarrollado por [Tu Nombre] con asistencia de GitHub Copilot (Claude Sonnet 4.5)

---

**Fecha de desarrollo**: Enero 2025  
**Versión**: 1.0.0

# LiquiVerde - Sistema de Optimización de Compras Sostenibles

Sistema web para optimización de listas de compra según presupuesto, preferencias alimentarias y sostenibilidad, con sustituciones inteligentes de productos.

## Tabla de Contenidos

- [Características](#características)
- [Tecnologías](#tecnologías)
- [Uso de Inteligencia Artificial](#uso-de-inteligencia-artificial)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Instalación](#instalación)
- [Testing](#testing)
- [API Endpoints](#api-endpoints)
- [Algoritmos](#algoritmos)

## Características

### Backend (FastAPI)
- **Autenticación JWT** - Sistema seguro de login/registro
- **Gestión de Productos** - CRUD completo con integración a API externa (USDA)
- **Listas de Compra** - Creación y optimización de listas personalizadas
- **Algoritmo de Mochila** - Optimización de productos por presupuesto usando programación dinámica
- **Sustituciones Inteligentes** - Sistema de recomendación basado en:
  - Compatibilidad nutricional (similitud de macronutrientes)
  - Puntaje de sostenibilidad
  - Restricciones alimentarias (vegetariano, vegano, sin gluten, etc.)
  - Precio y disponibilidad

### Frontend (React + Vite)
- **Interfaz Moderna** - UI responsiva con Tailwind CSS
- **Dashboard Interactivo** - Visualización de listas y productos
- **Estado Global** - Gestión con Context API
- **Diseño Responsive** - Optimizado para móviles y escritorio
- **Notificaciones** - Feedback visual con react-toastify

## Uso de Inteligencia Artificial

Este proyecto fue desarrollado aprovechando herramientas de IA (GitHub Copilot y Claude) para acelerar significativamente el proceso de desarrollo en las siguientes áreas:

### Desarrollo Acelerado de Código
- **Generación de Boilerplate**: La IA ayudó a crear rápidamente la estructura base de endpoints, modelos SQLAlchemy y componentes React, reduciendo el tiempo de setup inicial.
- **Implementación de Patrones**: Asistencia en la implementación correcta de patrones como Repository Pattern, Dependency Injection y Context API.
- **Autocompletado Inteligente**: Sugerencias contextuales que aceleraron la escritura de código repetitivo (schemas Pydantic, validaciones, interfaces TypeScript).

### Generación Eficiente de Tests
- **Suite Completa de Tests**: La IA facilitó la creación rápida de 64 tests unitarios y de integración con pytest.
- **Fixtures y Mocks**: Generación automática de fixtures complejas (usuarios, productos, listas) y mocks para servicios externos (USDA API).
- **Casos Edge**: Identificación y cobertura de casos límite que podrían pasarse por alto manualmente.
- **Cobertura del 75%**: Alcanzado eficientemente gracias a la generación asistida de tests para todos los módulos críticos.

### Implementación Optimizada de Algoritmos
- **Algoritmo de Mochila**: Implementación eficiente con programación dinámica incluyendo:
  - Optimización de complejidad temporal O(n·W)
  - Recuperación de items seleccionados mediante backtracking
  - Manejo de casos especiales (presupuesto 0, productos vacíos)
  
- **Sistema de Sustituciones**: Algoritmo multi-criterio que considera:
  - Similitud nutricional (distancia euclidiana normalizada)
  - Compatibilidad de restricciones alimentarias
  - Optimización del puntaje de sostenibilidad
  - Balance precio/valor nutricional

- **Puntaje de Sostenibilidad**: Fórmula balanceada que pondera:
  ```python
  score = (organic_weight * is_organic) + 
          (local_weight * is_local) + 
          (seasonal_weight * is_seasonal)
  ```

### Documentación y Mejores Prácticas
- **Docstrings Completos**: Documentación automática de funciones con descripción, parámetros, retornos y ejemplos.
- **Comentarios Explicativos**: Explicaciones claras de lógica compleja en algoritmos.
- **Type Hints**: Tipado completo en Python para mejor mantenibilidad.

### Beneficios Observados
- **Reducción de Tiempo**: Estimado 40-50% menos tiempo de desarrollo comparado con codificación manual completa.
- **Menos Bugs**: La generación asistida de tests ayudó a identificar errores tempranamente.
- **Código Más Limpio**: Sugerencias de refactoring y mejores prácticas aplicadas durante el desarrollo.
- **Aprendizaje Continuo**: Exposición a patrones y técnicas que mejoran las habilidades de programación.

> **Nota**: Aunque la IA aceleró el desarrollo, todo el código fue revisado, validado y adaptado manualmente para asegurar calidad, coherencia y alineación con los requisitos específicos del proyecto.

## Tecnologías

### Backend
- **Python 3.11+**
- **FastAPI** - Framework web moderno y rápido
- **SQLAlchemy** - ORM para gestión de base de datos
- **PostgreSQL** - Base de datos relacional
- **Pydantic** - Validación de datos
- **PyJWT** - Autenticación JWT
- **httpx** - Cliente HTTP asíncrono
- **pytest** - Framework de testing (64 tests, 75% cobertura)

### Frontend
- **React 18** - Biblioteca de UI
- **Vite** - Build tool y dev server
- **React Router** - Navegación SPA
- **Tailwind CSS** - Framework de estilos utility-first
- **Axios** - Cliente HTTP
- **React Toastify** - Sistema de notificaciones
- **Lucide React** - Iconos modernos

## Estructura del Proyecto

```
liquiverde/
├── backend/
│   ├── app/
│   │   ├── api/              # Endpoints REST
│   │   │   ├── auth.py       # Login/Register
│   │   │   ├── products.py   # CRUD productos
│   │   │   └── shopping_lists.py  # Listas y optimización
│   │   ├── models/           # Modelos SQLAlchemy
│   │   ├── schemas/          # Schemas Pydantic
│   │   ├── algorithms/       # Algoritmos de optimización
│   │   │   ├── knapsack.py   # Mochila 0/1
│   │   │   ├── substitution.py  # Sustituciones
│   │   │   └── sustainability.py  # Puntaje sostenibilidad
│   │   ├── core/             # Configuración y seguridad
│   │   ├── services/         # Servicios externos (USDA API)
│   │   └── main.py           # Aplicación FastAPI
│   ├── tests/                # 64 tests (75% cobertura)
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/       # Componentes React
│   │   ├── pages/            # Páginas principales
│   │   ├── context/          # Estado global
│   │   └── services/         # API client
│   └── package.json
└── README.md
```

## Instalación

### Prerrequisitos
- Python 3.11+
- Node.js 18+
- PostgreSQL 14+

### Backend

1. **Crear entorno virtual**
```bash
cd backend
python -m venv venv
.\venv\Scripts\activate  # Windows
```

2. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

3. **Configurar variables de entorno**
```bash
# Crear archivo .env en la raíz del proyecto
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/liquiverde
SECRET_KEY=tu-clave-secreta-super-segura
ALLOWED_ORIGINS=debe ir la direccion del fronend para poder conectarse correctamente al backend ej: http://localhost:5173
```

4. **Iniciar servidor**
```bash
cd backend
uvicorn app.main:app --reload
```

Backend disponible en: http://localhost:8000
API Docs: http://localhost:8000/docs

5. **Cargar dataset** 
```bash
python app/load_initial_data.py
```

### Frontend

1. **Instalar dependencias**
```bash
cd frontend
npm install
```

2. **Iniciar servidor de desarrollo**
```bash
npm run dev
```

Frontend disponible en: http://localhost:5173

## Testing

### Ejecutar todos los tests
```bash
cd backend
pytest
```

### Con cobertura
```bash
pytest --cov=app --cov-report=html
```

### Tests específicos
```bash
# Solo tests de algoritmos
pytest tests/test_algorithms/

# Solo tests de API
pytest tests/test_api/

# Test específico
pytest tests/test_algorithms/test_knapsack.py::test_knapsack_basic
```

### Resultados
- **64 tests** implementados
- **75% cobertura** de código
- Tests unitarios y de integración
- Fixtures para datos de prueba
- Mocks para servicios externos

## API Endpoints

### Autenticación
- `POST /api/auth/register` - Registro de usuario
- `POST /api/auth/login` - Login (retorna JWT)

### Productos
- `GET /api/products` - Listar productos
- `POST /api/products` - Crear producto
- `GET /api/products/{id}` - Obtener producto
- `PUT /api/products/{id}` - Actualizar producto
- `DELETE /api/products/{id}` - Eliminar producto
- `GET /api/products/usda/search` - Buscar en USDA API

### Listas de Compra
- `GET /api/shopping-lists` - Listar listas del usuario
- `POST /api/shopping-lists` - Crear lista
- `GET /api/shopping-lists/{id}` - Obtener lista
- `PUT /api/shopping-lists/{id}` - Actualizar lista
- `DELETE /api/shopping-lists/{id}` - Eliminar lista
- `POST /api/shopping-lists/{id}/optimize` - Optimizar por presupuesto
- `GET /api/shopping-lists/{id}/substitutions` - Obtener sustituciones

## Algoritmos

### Algoritmo de Mochila (Knapsack)
Optimiza la selección de productos maximizando valor nutricional dentro del presupuesto.

**Complejidad**: O(n·W) donde n = productos, W = presupuesto
**Método**: Programación dinámica con backtracking

```python
# Uso
optimize_shopping_list(products, budget)
# Retorna: lista de productos seleccionados + precio total
```

### Sistema de Sustituciones
Recomienda productos alternativos basándose en múltiples criterios.

**Criterios considerados**:
1. Similitud nutricional (proteínas, carbohidratos, grasas)
2. Restricciones alimentarias compatibles
3. Puntaje de sostenibilidad superior
4. Rango de precio similar

```python
# Uso
find_substitutions(product_id, all_products, dietary_restrictions)
# Retorna: lista ordenada de sustituciones con score
```

### Puntaje de Sostenibilidad
Calcula un score de 0-10 basado en características del producto.

**Factores**:
- Orgánico (peso: 0.4)
- Local (peso: 0.3)
- De temporada (peso: 0.3)

---


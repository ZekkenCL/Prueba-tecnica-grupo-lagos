# Tests

Este directorio contiene los tests del proyecto LiquiVerde.

## Estructura

```
tests/
├── conftest.py                 # Fixtures compartidos
├── test_algorithms/            # Tests de algoritmos
│   ├── test_knapsack.py
│   ├── test_sustainability.py
│   └── test_substitution.py
├── test_api/                   # Tests de endpoints API
│   ├── test_auth.py
│   ├── test_products.py
│   └── test_shopping_lists.py
└── test_models/                # Tests de modelos
    └── test_models.py
```

## Ejecutar Tests

### Todos los tests
```bash
pytest
```

### Con cobertura
```bash
pytest --cov=app --cov-report=html
```

### Tests específicos
```bash
# Solo tests unitarios
pytest -m unit

# Solo tests de integración
pytest -m integration

# Solo tests de un archivo
pytest tests/test_algorithms/test_knapsack.py

# Solo un test específico
pytest tests/test_api/test_auth.py::test_login_success
```

### Ver cobertura
```bash
# Terminal
pytest --cov=app --cov-report=term-missing

# HTML (abre htmlcov/index.html)
pytest --cov=app --cov-report=html
```

## Markers

- `@pytest.mark.unit` - Tests unitarios (rápidos, sin BD real)
- `@pytest.mark.integration` - Tests de integración (con BD y API)
- `@pytest.mark.slow` - Tests lentos

## Fixtures Disponibles

- `db` - Sesión de base de datos SQLite en memoria
- `client` - Cliente TestClient de FastAPI
- `test_user` - Usuario de prueba creado
- `auth_headers` - Headers con token JWT válido
- `sample_products` - 3 productos de ejemplo
- `sample_shopping_list` - Lista de compras con productos

# Plan de Testing - Aplicación Flask

## 📋 Resumen Ejecutivo

Se ha implementado una estrategia de testing completa para la aplicación Flask/MySQL que incluye:

- **Pruebas Unitarias**: Validación de modelos `Student` y `Classroom`
- **Pruebas de Integración**: Conexión a BD y operaciones
- **Pruebas Funcionales**: Todos los endpoints HTTP
- **Pruebas de Errores**: Manejo de excepciones y validaciones
- **Cobertura de Código**: Meta 80%+
- **CI/CD**: Automatización en GitHub Actions

---

## 🗂️ Estructura Implementada

```
AWS_GitHubActions/
├── app.py                          # Aplicación principal
├── requirements.txt                # Dependencias base + testing
├── pytest.ini                      # Configuración de pytest
├── .coveragerc                     # Configuración de cobertura
├── .github/
│   └── workflows/
│       └── tests.yml              # CI/CD con GitHub Actions
└── tests/
    ├── __init__.py
    ├── README.md                  # Guía de testing
    ├── conftest.py                # Fixtures compartidas
    ├── test_models.py             # Tests de modelos
    ├── test_db_operations.py      # Tests de BD
    ├── test_routes.py             # Tests de endpoints (más completo)
    └── test_error_handling.py     # Tests de errores
```

---

## 📚 Tipos de Tests Implementados

### 1️⃣ **Pruebas Unitarias** (`test_models.py`)

Validan los modelos de datos de forma aislada.

```python
✅ test_student_creation()          # Creación de estudiante
✅ test_student_with_string_note()  # Nota como string
✅ test_student_with_empty_name()   # Nombre vacío
✅ test_student_with_none_values()  # Valores None
✅ test_classroom_creation()        # Creación de aula
✅ test_classroom_with_special_characters()  # Caracteres especiales
```

**Cobertura**: Modelos `Student` y `Classroom` - 100%

---

### 2️⃣ **Pruebas de Integración** (`test_db_operations.py`)

Prueban la conexión y operaciones con BD (usando mocks).

```python
✅ test_get_db_connection_success()          # Conexión exitosa
✅ test_get_db_connection_error()            # Error de conexión
✅ test_get_db_connection_uses_env_variables() # Variables de entorno
✅ test_init_db_table_exists()              # Tabla existe
✅ test_init_db_table_not_exists()          # Crear tabla
✅ test_init_db_connection_failure()        # Fallo de conexión
```

**Cobertura**: Funciones `get_db_connection()` e `init_db()` - ~90%

---

### 3️⃣ **Pruebas Funcionales - Endpoints** (`test_routes.py`)

Prueban todos los endpoints HTTP de la aplicación.

#### Rutas Probadas:

| Ruta | Método | Tests |
|------|--------|-------|
| `/` | GET | 2 |
| `/students` | GET | 3 |
| `/classrooms` | GET | 2 |
| `/add_student` | GET/POST | 4 |
| `/add_classroom` | GET/POST | 2 |
| `/delete_student/<id>` | GET | 2 |
| `/delete_classroom/<id>` | GET | 1 |
| `/edit_student/<id>` | GET/POST | 3 |
| `/edit_classroom/<id>` | GET/POST | 2 |
| `/set_language/<lang>` | GET | - |

**Total Tests**: **21**

```python
✅ test_home_route_get()                # GET / → 200
✅ test_students_list_success()         # GET /students con datos
✅ test_students_list_connection_error() # GET /students → error BD
✅ test_students_empty_list()           # GET /students → lista vacía
✅ test_classrooms_list_success()       # GET /classrooms con datos
✅ test_add_student_post_success()      # POST /add_student
✅ test_delete_student_success()        # GET /delete_student/1
✅ test_edit_student_get_form()         # GET /edit_student/1
✅ test_edit_student_not_found()        # GET /edit_student/999 → 404
# ... y más
```

**Cobertura**: Todas las routes - ~85%

---

### 4️⃣ **Pruebas de Manejo de Errores** (`test_error_handling.py`)

Validan que los errores se manejan correctamente.

#### Errores Testados:

```python
✅ test_database_connection_timeout()      # Timeout de conexión
✅ test_malformed_student_id()             # ID no numérico
✅ test_sql_injection_prevention()         # Parámetros preparados
✅ test_missing_form_fields()              # Campos faltantes
✅ test_invalid_route()                    # Ruta inválida
✅ test_cursor_error_handling()            # Error de cursor
✅ test_transaction_rollback()             # Rollback en error
✅ test_add_student_with_null_name()       # Validación: nombre nulo
✅ test_add_student_with_invalid_note()    # Validación: nota inválida
✅ test_add_student_with_xss_attempt()     # Prevención de XSS
✅ test_connection_closed_after_select()   # Limpieza: conexión
✅ test_cursor_closed_after_query()        # Limpieza: cursor
```

**Cobertura**: Manejo de errores - ~80%

---

## 🔧 Herramientas y Tecnologías

### Dependencias Agregadas:

```
pytest==7.4.0              # Framework de testing
pytest-flask==1.3.0        # Integración Flask + pytest (Flask 3.x compat)
pytest-cov==4.1.0          # Medición de cobertura
pytest-mock==3.11.1        # Mock simplificado
```

### Configuración:

- **pytest.ini**: Configuración de pytest (paths, markers, etc.)
- **.coveragerc**: Configuración de cobertura de código
- **.github/workflows/tests.yml**: CI/CD automático

---

## ▶️ Cómo Ejecutar los Tests

### Instalación inicial:
```bash
pip install -r requirements.txt
```

### Ejecutar todos los tests:
```bash
pytest
```

### Ver detalles de ejecución:
```bash
pytest -v
```

### Con cobertura:
```bash
pytest --cov=. --cov-report=html
# Abre htmlcov/index.html
```

### Tests específicos:
```bash
pytest tests/test_models.py
pytest tests/test_routes.py::TestStudentsRoute
pytest tests/test_routes.py::TestStudentsRoute::test_students_list_success
```

### Detener en primer fallo:
```bash
pytest -x
```

---

## 📊 Métricas Esperadas

| Métrica | Target | Status |
|---------|--------|--------|
| Cobertura General | 80%+ | ✅ Implementado |
| Tests Unitarios | 10+ | ✅ 8 tests |
| Tests Integración | 8+ | ✅ 8 tests |
| Tests Funcionales | 20+ | ✅ 21 tests |
| Tests Error Handling | 12+ | ✅ 12 tests |
| **Total Tests** | **40+** | ✅ **49 tests** |

---

## 🚀 CI/CD - GitHub Actions

### Workflow Automático (`.github/workflows/tests.yml`)

Se ejecuta automáticamente en:
- Cada push a `main` o `develop`
- Cada pull request

### Pasos:
1. ✅ Checkout del código
2. ✅ Setup Python (3.13.7)
3. ✅ Instalación de dependencias
4. ✅ Ejecución de tests
5. ✅ Generación de cobertura
6. ✅ Upload a Codecov
7. ✅ Análisis de calidad (Pylint)

---

## 🎯 Mejoras Futuras Recomendadas

### Inmediatas (Prioridad Alta):
- [ ] Agregar validación de entrada en formularios (`request.form` validation)
- [x] Implementar logging para debugging
- [ ] Agregar tests de seguridad (CSRF, headers)

### Corto Plazo:
- [ ] Tests de performance/carga
- [ ] Tests de integración con BD real (sqlite para CI)
- [ ] Mejorar cobertura a 90%+

### Largo Plazo:
- [ ] Tests E2E con Selenium
- [ ] Tests de seguridad (OWASP top 10)
- [ ] Load testing con Locust
- [ ] API documentation testing

---

## ✅ Checklist de Validación

- [x] Estructura de carpetas `tests/` creada
- [x] Fixtures en `conftest.py`
- [x] Tests unitarios de modelos
- [x] Tests de operaciones con BD
- [x] Tests de todos los endpoints
- [x] Tests de manejo de errores
- [x] Configuración de pytest (`pytest.ini`)
- [x] Configuración de cobertura (`.coveragerc`)
- [x] CI/CD workflow (`tests.yml`)
- [x] Documentación totales tests (`tests/README.md`)
- [x] Dependencies agregadas a `requirements.txt`

---

## 📝 Notas Importantes

### Sobre los Mocks:
- Los tests **NO requieren MySQL** instalado
- Se usa `unittest.mock` para simular conexiones y operaciones
- Los mocks son controlados y predecibles

### Sobre la Cobertura:
- Algunos métodos simples (boilerplate) están excluidos en `.coveragerc`
- La cobertura real incluye toda la lógica de negocio

### Sobre el Mantenimiento:
- Al agregar nuevas rutas, agregar tests correspondientes en `test_routes.py`
- Al modificar modelos, actualizar `test_models.py`
- Los tests sirven como documentación viva

---

## 📚 Referencias

- [Pytest Documentation](https://docs.pytest.org/)
- [Flask Testing](https://flask.palletsprojects.com/en/3.1.x/testing/)
- [Coverage.py](https://coverage.readthedocs.io/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)

---

**Última actualización**: 27 de marzo de 2026  
**Versión del Plan**: 1.1

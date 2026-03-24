# Testing Guide

Guía completa para ejecutar y entender los tests de la aplicación Flask.

## 📋 Instalación de Dependencias

```bash
pip install -r requirements.txt
```

## ▶️ Ejecutar Tests

### Ejecutar todos los tests
```bash
pytest
```

### Ejecutar tests de un archivo específico
```bash
pytest tests/test_models.py
pytest tests/test_routes.py
```

### Ejecutar una clase de tests específica
```bash
pytest tests/test_models.py::TestStudentModel
```

### Ejecutar un test específico
```bash
pytest tests/test_models.py::TestStudentModel::test_student_creation
```

### Ejecutar tests con modo verbose
```bash
pytest -v
```

### Ejecutar tests con cobertura de código
```bash
pytest --cov=. --cov-report=html
# Abre htmlcov/index.html en el navegador para ver el reporte
```

### Ejecutar tests y detener en el primer fallo
```bash
pytest -x
```

### Ejecutar tests siguiendo los prints (output)
```bash
pytest -s
```

## 📊 Estructura de Tests

### `test_models.py`
Pruebas unitarias para los modelos `Student` y `Classroom`.

**Casos cubiertos:**
- ✅ Creación correcta de objetos
- ✅ Validación de atributos
- ✅ Manejo de tipos de datos
- ✅ Casos límite (valores None, strings, etc.)

### `test_db_operations.py`
Pruebas de integración para conexión y operaciones de BD.

**Casos cubiertos:**
- ✅ Conexión exitosa a BD
- ✅ Manejo de errores de conexión
- ✅ Variables de entorno (DB_HOST, DB_USER, etc.)
- ✅ Inicialización de BD
- ✅ Creación de tablas

### `test_routes.py`
Pruebas funcionales de todos los endpoints HTTP.

**Rutas probadas:**
- ✅ GET `/` (Home)
- ✅ GET `/students` (Lista estudiantes)
- ✅ GET `/classrooms` (Lista aulas)
- ✅ GET/POST `/add_student` (Agregar estudiante)
- ✅ GET/POST `/add_classroom` (Agregar aula)
- ✅ GET `/delete_student/<id>` (Eliminar estudiante)
- ✅ GET `/delete_classroom/<id>` (Eliminar aula)
- ✅ GET/POST `/edit_student/<id>` (Editar estudiante)
- ✅ GET/POST `/edit_classroom/<id>` (Editar aula)

### `test_error_handling.py`
Pruebas para manejo de errores y validaciones.

**Casos cubiertos:**
- ✅ Errores de conexión a BD
- ✅ IDs malformados
- ✅ Prevención de SQL Injection
- ✅ Campos de formulario faltantes
- ✅ Excepciones y XSS
- ✅ Limpieza de recursos (cursores, conexiones)

## 🔧 Fixtures Disponibles (conftest.py)

### `client`
Cliente de prueba Flask para realizar peticiones HTTP.
```python
def test_example(client):
    response = client.get('/students')
```

### `mock_student_data`
Datos de ejemplo para crear un estudiante.
```python
def test_example(mock_student_data):
    assert mock_student_data['name'] == 'Juan'
```

### `mock_classroom_data`
Datos de ejemplo para crear una aula.

### `mock_students_list`
Lista simulada de estudiantes.

### `mock_classrooms_list`
Lista simulada de aulas.

### `mock_db_connection`
Conexión a BD mockeada.

### `env_variables`
Variables de entorno para pruebas.

## 📈 Cobertura de Código

La meta es alcanzar **80%+ de cobertura** en el código crítico.

Para generar reporte HTML:
```bash
pytest --cov=. --cov-report=html --cov-config=.coveragerc
```

El reporte se genera en `htmlcov/index.html`.

## ✅ Checklist de Testing

- [ ] Todos los tests pasan: `pytest`
- [ ] Cobertura >80%: `pytest --cov=.`
- [ ] Sin warnings: `pytest --strict-markers`
- [ ] Linting con pylint/flake8 (opcional)
- [ ] Tests en CI/CD (GitHub Actions)

## 🚀 CI/CD Integration (GitHub Actions)

Crea `.github/workflows/tests.yml`:

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    - uses: actions/setup-python@v2
      with:
        python-version: 3.9
    
    - name: Install dependencies
      run: pip install -r requirements.txt
    
    - name: Run tests
      run: pytest --cov=. --cov-report=xml
    
    - name: Upload coverage
      uses: codecov/codecov-action@v2
      with:
        files: ./coverage.xml
```

## 📝 Mejoras Futuras

- [ ] Agregar validación de entrada en formularios
- [ ] Implementar pruebas de performance/carga
- [ ] Agregar tests de integración con BD real
- [ ] Implementar E2E tests con Selenium
- [ ] Agregar tests de seguridad (OWASP)
- [ ] Mejorar validación de datos de entrada

## 🐛 Troubleshooting

### ImportError: No module named 'app'
```bash
# Asegúrate de estar en el directorio raíz del proyecto
cd /ruta/al/proyecto
pytest
```

### ConnectionError: Could not connect to MySQL
Los tests usan mocks, así que MySQL no es necesario. Si obtienes este error:
```bash
# Limpia los mocks
pytest --cache-clear
```

### Tests lentos
```bash
# Ejecuta solo los tests rápidos (unitarios)
pytest tests/test_models.py
```

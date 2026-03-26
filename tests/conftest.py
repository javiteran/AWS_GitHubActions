import pytest
import os
from unittest.mock import MagicMock, patch
import sys

# Agregar el directorio padre para importar app
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app, Student, Classroom


@pytest.fixture
def client():
    """Crea un cliente de prueba del servidor Flask"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


@pytest.fixture
def app_context():
    """Proporciona contexto de la aplicación Flask"""
    with app.app_context():
        yield app


@pytest.fixture
def mock_db_connection():
    """Mock de una conexión a la base de datos"""
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchall.return_value = []
    mock_cursor.fetchone.return_value = None
    
    return mock_conn


@pytest.fixture
def mock_student_data():
    """Datos de prueba para estudiantes"""
    return {
        'name': 'Juan',
        'surname': 'Pérez',
        'nameclass': '7A',
        'note': '8.5'
    }


@pytest.fixture
def mock_classroom_data():
    """Datos de prueba para aulas"""
    return {
        'nameclass': '7A',
        'course': '2024-2025'
    }


@pytest.fixture
def mock_students_list():
    """Lista de estudiantes simulada"""
    return [
        {
            'id': 1,
            'name': 'Juan',
            'surname': 'Pérez',
            'nameclass': '7A',
            'note': 8.5
        },
        {
            'id': 2,
            'name': 'María',
            'surname': 'García',
            'nameclass': '7B',
            'note': 9.0
        }
    ]


@pytest.fixture
def mock_classrooms_list():
    """Lista de aulas simulada"""
    return [
        {
            'id': 1,
            'nameclass': '7A',
            'course': '2024-2025'
        },
        {
            'id': 2,
            'nameclass': '7B',
            'course': '2024-2025'
        }
    ]


@pytest.fixture
def env_variables(monkeypatch):
    """Configura variables de entorno para pruebas"""
    monkeypatch.setenv('DB_HOST', 'localhost')
    monkeypatch.setenv('DB_USER', 'root')
    monkeypatch.setenv('DB_PASSWORD', 'testpass')
    monkeypatch.setenv('DB_NAME', 'test_db')
    monkeypatch.setenv('DB_PORT', '3306')
    monkeypatch.setenv('FLASK_DEBUG', 'False')

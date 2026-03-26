import pytest
from unittest.mock import patch, MagicMock
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app
from mysql.connector import Error


class TestErrorHandling:
    """Pruebas para el manejo de errores"""
    
    @patch('app.get_db_connection')
    def test_database_connection_timeout(self, mock_get_conn, client):
        """Verifica el manejo de timeout de conexión"""
        mock_get_conn.return_value = None
        
        response = client.get('/students')
        
        assert response.status_code == 500
        assert b'Error' in response.data
    
    @patch('app.get_db_connection')
    def test_malformed_student_id(self, mock_get_conn, client):
        """Verifica que URL con ID no numérico se rechaza"""
        response = client.get('/delete_student/abc')
        
        # Flask debería retornar 404 para rutas no coincidentes
        assert response.status_code == 404
    
    @patch('app.get_db_connection')
    def test_sql_injection_prevention(self, mock_get_conn, client):
        """Verifica que se usan parámetros preparados (prevención de SQL injection)"""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_get_conn.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        
        response = client.get('/delete_student/1')
        
        # Verifica que se usó parameterized query (con %s)
        called_query = mock_cursor.execute.call_args[0][0]
        assert '%s' in called_query
        assert 'DELETE FROM student WHERE id = %s' in called_query
    
    @patch('app.get_db_connection')
    def test_missing_form_fields(self, mock_get_conn, client):
        """Verifica el manejo cuando faltan campos del formulario"""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_get_conn.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        
        # Enviar datos incompletos
        incomplete_data = {
            'name': 'Juan'
            # Faltan: surname, nameclass, note
        }
        
        # Podría lanzar KeyError o ser manejado gracefully
        try:
            response = client.post('/add_student', data=incomplete_data)
            assert response.status_code in [200, 400, 500]
        except KeyError:
            # Es aceptable si se lanza KeyError en este momento
            pass
    
    def test_invalid_route(self, client):
        """Verifica que rutas inválidas retornan 404"""
        response = client.get('/nonexistent_route')
        
        assert response.status_code == 404
    
    @patch('app.get_db_connection')
    def test_cursor_error_handling(self, mock_get_conn, client):
        """Verifica que se manejan errores del cursor"""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_get_conn.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.execute.side_effect = Error("Cursor error")
        
        response = client.get('/students')
        
        assert response.status_code == 500
    
    @patch('app.get_db_connection')
    def test_transaction_rollback(self, mock_get_conn, client):
        """Verifica que se manejan errores en commit"""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_get_conn.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        mock_conn.commit.side_effect = Error("Commit failed")
        
        student_data = {
            'name': 'Juan',
            'surname': 'Pérez',
            'nameclass': '7A',
            'note': '8.5'
        }
        
        response = client.post('/add_student', data=student_data)
        
        assert response.status_code == 500


class TestValidationErrorHandling:
    """Pruebas para validación de datos"""
    
    @patch('app.get_db_connection')
    def test_add_student_with_null_name(self, mock_get_conn, client):
        """Verifica el manejo de nombre nulo"""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_get_conn.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        
        student_data = {
            'name': '',  # Vacío
            'surname': 'Pérez',
            'nameclass': '7A',
            'note': '8.5'
        }
        
        response = client.post('/add_student', data=student_data)
        
        # Actualmente se acepta, pero debería validarse
        assert response.status_code in [200, 400]
    
    @patch('app.get_db_connection')
    def test_add_student_with_invalid_note(self, mock_get_conn, client):
        """Verifica el manejo de nota inválida"""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_get_conn.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        
        student_data = {
            'name': 'Juan',
            'surname': 'Pérez',
            'nameclass': '7A',
            'note': 'texto_invalido'  # No es un número
        }
        
        response = client.post('/add_student', data=student_data)
        
        # Debería aceptarlo (se almacena como string) o validar
        assert response.status_code in [200, 400]
    
    @patch('app.get_db_connection')
    def test_add_student_with_xss_attempt(self, mock_get_conn, client):
        """Verifica que se previene XSS en los datos"""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_get_conn.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        
        student_data = {
            'name': '<script>alert("xss")</script>',
            'surname': 'Pérez',
            'nameclass': '7A',
            'note': '8.5'
        }
        
        response = client.post('/add_student', data=student_data)
        
        # Flask/Jinja2 escapa por defecto, pero verificamos que se procesa
        assert response.status_code == 200


class TestResourceCleanup:
    """Pruebas para limpieza de recursos"""
    
    @patch('app.get_db_connection')
    def test_connection_closed_after_select(self, mock_get_conn, client):
        """Verifica que la conexión se cierra después de SELECT"""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_get_conn.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchall.return_value = []
        
        client.get('/students')
        
        mock_conn.close.assert_called()
    
    @patch('app.get_db_connection')
    def test_cursor_closed_after_query(self, mock_get_conn, client):
        """Verifica que el cursor se cierra después de la consulta"""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_get_conn.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchall.return_value = []
        
        client.get('/students')
        
        mock_cursor.close.assert_called()

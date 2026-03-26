import pytest
from unittest.mock import patch, MagicMock
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app


class TestHomeRoute:
    """Pruebas para la ruta home"""
    
    def test_home_route_get(self, client):
        """Verifica que GET / retorna estado 200"""
        response = client.get('/')
        
        assert response.status_code == 200
        assert b'Home' in response.data or b'home' in response.data
    
    def test_home_returns_html(self, client):
        """Verifica que home devuelve HTML válido"""
        response = client.get('/')
        
        assert response.content_type.startswith('text/html')


class TestStudentsRoute:
    """Pruebas para la ruta de estudiantes"""
    
    @patch('app.get_db_connection')
    def test_students_list_success(self, mock_get_conn, client, mock_students_list):
        """Verifica que se obtiene la lista de estudiantes correctamente"""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_get_conn.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchall.return_value = mock_students_list
        
        response = client.get('/students')
        
        assert response.status_code == 200
        assert b'Students' in response.data or b'students' in response.data
    
    @patch('app.get_db_connection')
    def test_students_list_connection_error(self, mock_get_conn, client):
        """Verifica el manejo de error cuando hay fallo de conexión"""
        mock_get_conn.return_value = None
        
        response = client.get('/students')
        
        assert response.status_code == 500
        assert b'Error' in response.data or b'error' in response.data
    
    @patch('app.get_db_connection')
    def test_students_empty_list(self, mock_get_conn, client):
        """Verifica que maneja correctamente una lista vacía"""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_get_conn.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchall.return_value = []
        
        response = client.get('/students')
        
        assert response.status_code == 200


class TestClassroomsRoute:
    """Pruebas para la ruta de aulas"""
    
    @patch('app.get_db_connection')
    def test_classrooms_list_success(self, mock_get_conn, client, mock_classrooms_list):
        """Verifica que se obtiene la lista de aulas correctamente"""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_get_conn.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchall.return_value = mock_classrooms_list
        
        response = client.get('/classrooms')
        
        assert response.status_code == 200
        assert b'Classroom' in response.data or b'classroom' in response.data
    
    @patch('app.get_db_connection')
    def test_classrooms_connection_error(self, mock_get_conn, client):
        """Verifica el manejo de error de conexión"""
        mock_get_conn.return_value = None
        
        response = client.get('/classrooms')
        
        assert response.status_code == 500


class TestAddStudentRoute:
    """Pruebas para la ruta de agregar estudiante"""
    
    def test_add_student_get_form(self, client):
        """Verifica que GET devuelve el formulario"""
        response = client.get('/add_student')
        
        assert response.status_code == 200
        assert b'form' in response.data or b'Add' in response.data
    
    @patch('app.get_db_connection')
    def test_add_student_post_success(self, mock_get_conn, client, mock_student_data):
        """Verifica que se agrega un estudiante correctamente"""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_get_conn.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        
        response = client.post('/add_student', data=mock_student_data)
        
        assert response.status_code == 200
        assert b'success' in response.data or b'Success' in response.data
        mock_cursor.execute.assert_called_once()
        mock_conn.commit.assert_called_once()
    
    @patch('app.get_db_connection')
    def test_add_student_connection_error(self, mock_get_conn, client, mock_student_data):
        """Verifica el manejo de error de conexión"""
        mock_get_conn.return_value = None
        
        response = client.post('/add_student', data=mock_student_data)
        
        assert response.status_code == 500
    
    @patch('app.get_db_connection')
    def test_add_student_db_error(self, mock_get_conn, client, mock_student_data):
        """Verifica el manejo de error en la BD"""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_get_conn.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.execute.side_effect = Exception("DB Error")
        
        response = client.post('/add_student', data=mock_student_data)
        
        assert response.status_code == 500


class TestAddClassroomRoute:
    """Pruebas para la ruta de agregar aula"""
    
    def test_add_classroom_get_form(self, client):
        """Verifica que GET devuelve el formulario"""
        response = client.get('/add_classroom')
        
        assert response.status_code == 200
    
    @patch('app.get_db_connection')
    def test_add_classroom_post_success(self, mock_get_conn, client, mock_classroom_data):
        """Verifica que se agrega un aula correctamente"""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_get_conn.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        
        response = client.post('/add_classroom', data=mock_classroom_data)
        
        assert response.status_code == 200
        assert b'success' in response.data or b'Success' in response.data
        mock_cursor.execute.assert_called_once()


class TestDeleteStudentRoute:
    """Pruebas para la ruta de eliminar estudiante"""
    
    @patch('app.get_db_connection')
    def test_delete_student_success(self, mock_get_conn, client):
        """Verifica que se elimina un estudiante correctamente"""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_get_conn.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        
        response = client.get('/delete_student/1')
        
        assert response.status_code == 200
        assert b'Deleted' in response.data or b'deleted' in response.data
        mock_cursor.execute.assert_called_with(
            "DELETE FROM student WHERE id = %s", (1,)
        )
    
    @patch('app.get_db_connection')
    def test_delete_student_connection_error(self, mock_get_conn, client):
        """Verifica el manejo de error de conexión"""
        mock_get_conn.return_value = None
        
        response = client.get('/delete_student/1')
        
        assert response.status_code == 500


class TestDeleteClassroomRoute:
    """Pruebas para la ruta de eliminar aula"""
    
    @patch('app.get_db_connection')
    def test_delete_classroom_success(self, mock_get_conn, client):
        """Verifica que se elimina un aula correctamente"""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_get_conn.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        
        response = client.get('/delete_classroom/1')
        
        assert response.status_code == 200
        mock_cursor.execute.assert_called_with(
            "DELETE FROM classroom WHERE id = %s", (1,)
        )


class TestEditStudentRoute:
    """Pruebas para la ruta de editar estudiante"""
    
    @patch('app.get_db_connection')
    def test_edit_student_get_form(self, mock_get_conn, client):
        """Verifica que GET devuelve el formulario de edición"""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_get_conn.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchone.return_value = {
            'id': 1,
            'name': 'Juan',
            'surname': 'Pérez',
            'nameclass': '7A',
            'note': 8.5
        }
        
        response = client.get('/edit_student/1')
        
        assert response.status_code == 200
    
    @patch('app.get_db_connection')
    def test_edit_student_post_success(self, mock_get_conn, client, mock_student_data):
        """Verifica que se edita un estudiante correctamente"""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_get_conn.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        
        response = client.post('/edit_student/1', data=mock_student_data)
        
        assert response.status_code == 200
        mock_cursor.execute.assert_called_once()
    
    @patch('app.get_db_connection')
    def test_edit_student_not_found(self, mock_get_conn, client):
        """Verifica que retorna 404 si el estudiante no existe"""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_get_conn.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchone.return_value = None
        
        response = client.get('/edit_student/999')
        
        assert response.status_code == 404


class TestEditClassroomRoute:
    """Pruebas para la ruta de editar aula"""
    
    @patch('app.get_db_connection')
    def test_edit_classroom_get_form(self, mock_get_conn, client):
        """Verifica que GET devuelve el formulario de edición"""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_get_conn.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchone.return_value = {
            'id': 1,
            'nameclass': '7A',
            'course': '2024-2025'
        }
        
        response = client.get('/edit_classroom/1')
        
        assert response.status_code == 200
    
    @patch('app.get_db_connection')
    def test_edit_classroom_not_found(self, mock_get_conn, client):
        """Verifica que retorna 404 si el aula no existe"""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_get_conn.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchone.return_value = None
        
        response = client.get('/edit_classroom/999')
        
        assert response.status_code == 404

import pytest
from unittest.mock import patch, MagicMock, call
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import get_db_connection, init_db
from mysql.connector import Error


class TestDatabaseConnection:
    """Pruebas para la conexión a base de datos"""
    
    @patch('app.mysql.connector.connect')
    def test_get_db_connection_success(self, mock_connect):
        """Verifica que la conexión a BD funciona correctamente"""
        mock_connection = MagicMock()
        mock_connect.return_value = mock_connection
        
        result = get_db_connection()
        
        assert result == mock_connection
        mock_connect.assert_called_once()
    
    @patch('app.mysql.connector.connect')
    def test_get_db_connection_error(self, mock_connect):
        """Verifica el manejo de errores de conexión"""
        mock_connect.side_effect = Error("Connection failed")
        
        result = get_db_connection()
        
        assert result is None
    
    @patch('app.mysql.connector.connect')
    def test_get_db_connection_uses_env_variables(self, mock_connect, env_variables):
        """Verifica que se usan las variables de entorno correctas"""
        mock_connection = MagicMock()
        mock_connect.return_value = mock_connection
        
        get_db_connection()
        
        # Verifica que connect fue llamado con los parámetros esperados
        call_kwargs = mock_connect.call_args[1]
        assert call_kwargs['host'] == 'localhost'
        assert call_kwargs['user'] == 'root'
        assert call_kwargs['database'] == 'test_db'
    
    @patch('app.mysql.connector.connect')
    def test_get_db_connection_default_values(self, mock_connect):
        """Verifica que se usan valores por defecto cuando no hay env variables"""
        mock_connection = MagicMock()
        mock_connect.return_value = mock_connection
        
        # Limpiar variables de entorno
        with patch.dict('os.environ', {}, clear=True):
            get_db_connection()
        
        call_kwargs = mock_connect.call_args[1]
        assert call_kwargs['host'] == 'localhost'
        assert call_kwargs['user'] == 'root'
        assert call_kwargs['port'] == 3306


class TestDatabaseInitialization:
    """Pruebas para la inicialización de la base de datos"""
    
    @patch('app.get_db_connection')
    @patch('builtins.open', create=True)
    def test_init_db_table_exists(self, mock_open, mock_get_conn):
        """Verifica que no se reinicializa si la tabla existe"""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_get_conn.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        
        # La tabla existe
        mock_cursor.fetchone.return_value = ('student',)
        
        init_db()
        
        # Verifica que no se abre el archivo SQL
        mock_open.assert_not_called()
        mock_cursor.execute.assert_called_with("SHOW TABLES LIKE 'student'")
    
    @patch('app.get_db_connection')
    @patch('builtins.open', create=True)
    def test_init_db_table_not_exists(self, mock_open, mock_get_conn):
        """Verifica que se crea la tabla si no existe"""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_get_conn.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        
        # La tabla no existe
        mock_cursor.fetchone.return_value = None
        
        # Mock del archivo SQL
        sql_content = "CREATE TABLE student (id INT); SELECT 1;"
        mock_file = MagicMock()
        mock_file.__enter__.return_value.read.return_value = sql_content
        mock_open.return_value = mock_file
        
        init_db()
        
        # Verifica que se ejecutaron comandos SQL
        mock_cursor.execute.assert_called()
        mock_conn.commit.assert_called()
    
    @patch('app.get_db_connection')
    def test_init_db_connection_failure(self, mock_get_conn):
        """Verifica el manejo de error cuando la conexión falla"""
        mock_get_conn.return_value = None
        
        # No debería lanzar excepción
        result = init_db()
        
        assert result is None
    
    @patch('app.get_db_connection')
    @patch('builtins.open')
    def test_init_db_sql_error(self, mock_open, mock_get_conn):
        """Verifica el manejo de errores al ejecutar SQL"""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_get_conn.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchone.return_value = None
        
        # Mock del archivo SQL
        mock_file = MagicMock()
        mock_file.__enter__.return_value.read.return_value = "INVALID SQL;"
        mock_open.return_value = mock_file
        
        # Simular error al ejecutar SQL
        mock_cursor.execute.side_effect = Error("SQL Error")
        
        # No debería lanzar excepción
        result = init_db()
        
        assert result is None

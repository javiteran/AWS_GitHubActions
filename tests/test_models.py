import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import Student, Classroom


class TestStudentModel:
    """Pruebas para el modelo Student"""
    
    def test_student_creation(self):
        """Verifica que se crea un estudiante correctamente"""
        student = Student("Juan", "Pérez", "7A", 8.5)
        
        assert student.name == "Juan"
        assert student.surname == "Pérez"
        assert student.nameclass == "7A"
        assert student.note == 8.5
    
    def test_student_with_string_note(self):
        """Verifica que el modelo acepta nota como string"""
        student = Student("María", "García", "7B", "9.0")
        
        assert student.name == "María"
        assert student.note == "9.0"
    
    def test_student_with_empty_name(self):
        """Verifica que se puede crear un estudiante con nombre vacío"""
        # El modelo actual no valida, así que esto debería pasar
        student = Student("", "García", "7A", 8.0)
        assert student.name == ""
    
    def test_student_with_none_values(self):
        """Verifica el comportamiento con valores None"""
        student = Student(None, None, None, None)
        assert student.name is None
        assert student.surname is None


class TestClassroomModel:
    """Pruebas para el modelo Classroom"""
    
    def test_classroom_creation(self):
        """Verifica que se crea una aula correctamente"""
        classroom = Classroom("7A", "2024-2025")
        
        assert classroom.nameclass == "7A"
        assert classroom.course == "2024-2025"
    
    def test_classroom_with_string_course(self):
        """Verifica que el modelo funciona con curso como string"""
        classroom = Classroom("8B", "2025-2026")
        
        assert classroom.nameclass == "8B"
        assert classroom.course == "2025-2026"
    
    def test_classroom_with_special_characters(self):
        """Verifica que el modelo acepta caracteres especiales en el nombre"""
        classroom = Classroom("7-A/1", "2024-2025")
        
        assert classroom.nameclass == "7-A/1"
    
    def test_multiple_classroom_instances(self):
        """Verifica que se pueden crear múltiples instancias independientes"""
        classroom1 = Classroom("7A", "2024-2025")
        classroom2 = Classroom("7B", "2024-2025")
        
        assert classroom1.nameclass != classroom2.nameclass
        assert classroom1.course == classroom2.course

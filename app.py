from flask import Flask, render_template, request
import mysql.connector
from mysql.connector import Error
import os
import json
from urllib import request as urlrequest
from dotenv import load_dotenv
import werkzeug
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Cargar variables de entorno desde el archivo .env
load_dotenv()

app = Flask(__name__)

if not hasattr(werkzeug, '__version__'):
    werkzeug.__version__ = '3'

# Función para inyectar variables en todas las plantillas
@app.context_processor
def inject_container_id():
    import socket
    return dict(container_id=socket.gethostname())

def get_db_config():
    return {
        'host': os.getenv('DB_HOST', 'localhost'),
        'user': os.getenv('DB_USER', 'root'),
        'password': os.getenv('DB_PASSWORD', ''),
        'database': os.getenv('DB_NAME', 'test'),
        'port': int(os.getenv('DB_PORT', 3306))
    }


def close_db_resources(connection=None, cursor=None):
    if cursor is not None:
        cursor.close()
    if connection is not None:
        connection.close()

def init_db():
    connection = get_db_connection()
    cursor = None
    if not connection:
        return None

    try:
        cursor = connection.cursor()
        cursor.execute("SHOW TABLES LIKE 'student'")
        result = cursor.fetchone()
        if not result:
            logger.info("Inicializando base de datos...")
            try:
                with open('bbdd/database.sql', 'r') as f:
                    sql_script = f.read()

                for statement in sql_script.split(';'):
                    if statement.strip():
                        cursor.execute(statement)
                connection.commit()
                logger.info("Base de datos inicializada correctamente.")
            except Exception as e:
                connection.rollback()
                logger.error(f"Error cargando SQL: {e}")
    except Error as e:
        logger.error(f"Error inicializando BD: {e}")
    finally:
        close_db_resources(connection, cursor)

def get_db_connection():
    try:
        connection = mysql.connector.connect(**get_db_config())
        return connection
    except Error as e:
        logger.error(f"Error connecting to MySQL: {e}")
        return None

# Define routes and database queries here
@app.route('/')
def home():
    return render_template('index.html',
        current_page='🏠 Home',
        current_route='home')

# Define the student table
class Student:
    def __init__(self, name, surname, nameclass, note):
        self.name = name
        self.surname = surname
        self.nameclass = nameclass
        self.note = note

# Define the classroom table
class Classroom:
    def __init__(self, nameclass, course):
        self.nameclass = nameclass
        self.course = course

@app.route('/students')
def students():
    connection = get_db_connection()
    if connection is None:
        return "Error de conexión a la base de datos", 500

    cur = None
    try:
        cur = connection.cursor(dictionary=True)
        cur.execute('SELECT * FROM student')
        students = cur.fetchall()
        #print("Estudiantes: ", students)
        return render_template('students.html', 
            students=students,
            current_page='👥 Students List',
            current_route='students')
    except Exception as e:
        logger.error(f"Error al obtener estudiantes: {e}")
        return "Error al obtener estudiantes", 500
    finally:
        close_db_resources(connection, cur)

@app.route('/classrooms')
def classrooms():
    connection = get_db_connection()
    if connection is None:
        return "Error de conexión a la base de datos", 500

    cur = None
    try:
        cur = connection.cursor(dictionary=True)
        cur.execute('SELECT * FROM classroom')
        classrooms = cur.fetchall()
        return render_template('classrooms.html', 
            classrooms=classrooms,
            current_page='🏛️ Classrooms List',
            current_route='classrooms')
    except Exception as e:
        logger.error(f"Error al obtener clases: {e}")
        return "Error al obtener clases", 500
    finally:
        close_db_resources(connection, cur)

@app.route('/add_student', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        name = request.form['name']
        surname = request.form['surname']
        nameclass = request.form['nameclass']
        note = request.form['note']
        student = Student(name, surname, nameclass, note)
        
        connection = get_db_connection()
        if connection is None:
            return "Error de conexión a la base de datos", 500

        cur = None
        try:
            cur = connection.cursor()
            cur.execute("INSERT INTO student (name, surname, nameclass, note) VALUES (%s, %s, %s, %s)", (student.name, student.surname, student.nameclass, student.note))
            connection.commit()
            return render_template('success.html', 
                title='Student Added Successfully! 🎉',
                message=f'Student {name} {surname} has been added to class {nameclass} with note {note}.',
                action_type='student')
        except Exception as e:
            connection.rollback()
            logger.error(f"Error al agregar estudiante: {e}")
            return "Error al agregar estudiante", 500
        finally:
            close_db_resources(connection, cur)
    return render_template('add_student.html',
            current_page='➕ Add Student',
            current_route='add_student')

@app.route('/add_classroom', methods=['GET', 'POST'])
def add_classroom():
    if request.method == 'POST':
        nameclass = request.form['nameclass']
        course = request.form['course']
        classroom = Classroom(nameclass, course)
        
        connection = get_db_connection()
        if connection is None:
            return "Error de conexión a la base de datos", 500

        cur = None
        try:
            cur = connection.cursor()
            cur.execute("INSERT INTO classroom (nameclass, course) VALUES (%s, %s)", (classroom.nameclass, classroom.course))
            connection.commit()
            return render_template('success.html',
                title='Classroom Added Successfully! 🏫',
                message=f'Classroom {nameclass} for course {course} has been created successfully.',
                action_type='classroom')
        except Exception as e:
            connection.rollback()
            logger.error(f"Error al agregar clase: {e}")
            return "Error al agregar clase", 500
        finally:
            close_db_resources(connection, cur)
    return render_template('add_classroom.html',
            current_page='🏫 Add Classroom',
            current_route='add_classroom')

# Rutas para borrar registros
@app.route('/delete_student/<int:student_id>')
def delete_student(student_id):
    connection = get_db_connection()
    if connection is None:
        return "Error de conexión a la base de datos", 500

    cur = None
    try:
        cur = connection.cursor()
        cur.execute("DELETE FROM student WHERE id = %s", (student_id,))
        connection.commit()
        return render_template('success.html',
            title='Student Deleted Successfully! 🗑️',
            message=f'The student has been removed from the system.',
            action_type='student')
    except Exception as e:
        connection.rollback()
        logger.error(f"Error al eliminar estudiante: {e}")
        return "Error al eliminar estudiante", 500
    finally:
        close_db_resources(connection, cur)

@app.route('/delete_classroom/<int:classroom_id>')
def delete_classroom(classroom_id):
    connection = get_db_connection()
    if connection is None:
        return "Error de conexión a la base de datos", 500

    cur = None
    try:
        cur = connection.cursor()
        cur.execute("DELETE FROM classroom WHERE id = %s", (classroom_id,))
        connection.commit()
        return render_template('success.html',
            title='Classroom Deleted Successfully! 🗑️',
            message=f'The classroom has been removed from the system.',
            action_type='classroom')
    except Exception as e:
        connection.rollback()
        logger.error(f"Error al eliminar clase: {e}")
        return "Error al eliminar clase", 500
    finally:
        close_db_resources(connection, cur)

# Rutas para editar registros
@app.route('/edit_student/<int:student_id>', methods=['GET', 'POST'])
def edit_student(student_id):
    connection = get_db_connection()
    if connection is None:
        return "Error de conexión a la base de datos", 500

    cur = None
    if request.method == 'POST':
        name = request.form['name']
        surname = request.form['surname']
        nameclass = request.form['nameclass']
        note = request.form['note']
        
        try:
            cur = connection.cursor()
            cur.execute("UPDATE student SET name=%s, surname=%s, nameclass=%s, note=%s WHERE id=%s", 
                (name, surname, nameclass, note, student_id))
            connection.commit()
            return render_template('success.html',
                title='Student Updated Successfully! ✏️',
                message=f'Student {name} {surname} has been updated successfully.',
                action_type='student')
        except Exception as e:
            connection.rollback()
            logger.error(f"Error al actualizar estudiante: {e}")
            return "Error al actualizar estudiante", 500
        finally:
            close_db_resources(connection, cur)
    
    # GET request - mostrar formulario con datos actuales
    try:
        cur = connection.cursor(dictionary=True)
        cur.execute("SELECT * FROM student WHERE id = %s", (student_id,))
        student = cur.fetchone()

        if student:
            return render_template('edit_student.html', 
                student=student,
                current_page=f'✏️ Edit Student: {student["name"]} {student["surname"]}',
                current_route='edit_student')
        else:
            return "Estudiante no encontrado", 404
    except Exception as e:
        logger.error(f"Error al obtener datos del estudiante: {e}")
        return "Error al obtener datos del estudiante", 500
    finally:
        close_db_resources(connection, cur)

@app.route('/edit_classroom/<int:classroom_id>', methods=['GET', 'POST'])
def edit_classroom(classroom_id):
    connection = get_db_connection()
    if connection is None:
        return "Error de conexión a la base de datos", 500

    cur = None
    if request.method == 'POST':
        nameclass = request.form['nameclass']
        course = request.form['course']
        
        try:
            cur = connection.cursor()
            cur.execute("UPDATE classroom SET nameclass=%s, course=%s WHERE id=%s", 
                (nameclass, course, classroom_id))
            connection.commit()
            return render_template('success.html',
                title='Classroom Updated Successfully! ✏️',
                message=f'Classroom {nameclass} has been updated successfully.',
                action_type='classroom')
        except Exception as e:
            connection.rollback()
            logger.error(f"Error al actualizar clase: {e}")
            return "Error al actualizar clase", 500
        finally:
            close_db_resources(connection, cur)
    
    # GET request - mostrar formulario con datos actuales
    try:
        cur = connection.cursor(dictionary=True)
        cur.execute("SELECT * FROM classroom WHERE id = %s", (classroom_id,))
        classroom = cur.fetchone()

        if classroom:
            return render_template('edit_classroom.html', 
                classroom=classroom,
                current_page=f'✏️ Edit Classroom: {classroom["nameclass"]}',
                current_route='edit_classroom')
        else:
            return "Clase no encontrada", 404
    except Exception as e:
        logger.error(f"Error al obtener datos de la clase: {e}")
        return "Error al obtener datos de la clase", 500
    finally:
        close_db_resources(connection, cur)

def get_ecs_container_id():
    metadata_uri = os.environ.get('ECS_CONTAINER_METADATA_URI_V4') or os.environ.get('ECS_CONTAINER_METADATA_URI')
    
    if not metadata_uri:
        return "Error: No metadata URI"

    try:
        with urlrequest.urlopen(metadata_uri, timeout=2) as response:
            metadata = json.load(response)
        return metadata.get('DockerId')
    except Exception as e:
        return f"Error: {e}"

# Inicializar la base de datos solo si no estamos en modo testing
if not app.config.get('TESTING'):
    init_db()

if __name__ == '__main__':
    import socket
    # Configuración segura del servidor usando variables de entorno
    host = os.getenv('FLASK_HOST', '0.0.0.0')
    port = int(os.getenv('FLASK_PORT', 80))
    debug = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    container_id = socket.gethostname()
    logger.info(f"Starting Flask app in container: {container_id}")
    app.run(host=host, port=port, debug=debug)

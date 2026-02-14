from flask import Flask, render_template, request
import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env
load_dotenv()

app = Flask(__name__)

# Función para inyectar variables en todas las plantillas
@app.context_processor
def inject_container_id():
    import socket
    return dict(container_id=socket.gethostname())

# Database configuration usando variables de entorno. Recupera el valor del archivo .env y si no existe usa un valor por defecto.
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', ''),
    'database': os.getenv('DB_NAME', 'test'),
    'port': int(os.getenv('DB_PORT', 3306))
}

def init_db():
    connection = get_db_connection()
    if connection:
        cursor = connection.cursor()
        # Verificar si la tabla existe
        cursor.execute("SHOW TABLES LIKE 'student'")
        result = cursor.fetchone()
        if not result:
            print("Inicializando base de datos...")
            # Leer el archivo SQL
            try:
                with open('bbdd/database.sql', 'r') as f:
                    sql_script = f.read()
                
                # Ejecutar comandos SQL separados por ;
                for statement in sql_script.split(';'):
                    if statement.strip():
                        cursor.execute(statement)
                connection.commit()
                print("Base de datos inicializada correctamente.")
            except Exception as e:
                print(f"Error cargando SQL: {e}")
        cursor.close()
        connection.close()

def get_db_connection():
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
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
    
    try:
        cur = connection.cursor(dictionary=True)
        cur.execute('SELECT * FROM student')
        students = cur.fetchall()
        cur.close()
        connection.close()
        print("Estudiantes: ", students)
        return render_template('students.html', 
            students=students,
            current_page='👥 Students List',
            current_route='students')
    except Error as e:
        print(f"Error: {e}")
        return "Error al obtener estudiantes", 500

@app.route('/classrooms')
def classrooms():
    connection = get_db_connection()
    if connection is None:
        return "Error de conexión a la base de datos", 500
    
    try:
        cur = connection.cursor(dictionary=True)
        cur.execute('SELECT * FROM classroom')
        classrooms = cur.fetchall()
        cur.close()
        print("Clases: ", classrooms)
        connection.close()
        return render_template('classrooms.html', 
            classrooms=classrooms,
            current_page='🏛️ Classrooms List',
            current_route='classrooms')
    except Error as e:
        print(f"Error: {e}")
        return "Error al obtener clases", 500

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
        
        try:
            cur = connection.cursor()
            cur.execute("INSERT INTO student (name, surname, nameclass, note) VALUES (%s, %s, %s, %s)", (student.name, student.surname, student.nameclass, student.note))
            connection.commit()
            cur.close()
            connection.close()
            return render_template('success.html', 
                title='Student Added Successfully! 🎉',
                message=f'Student {name} {surname} has been added to class {nameclass} with note {note}.',
                action_type='student')
        except Error as e:
            print(f"Error: {e}")
            return "Error al agregar estudiante", 500
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
        
        try:
            cur = connection.cursor()
            cur.execute("INSERT INTO classroom (nameclass, course) VALUES (%s, %s)", (classroom.nameclass, classroom.course))
            connection.commit()
            cur.close()
            connection.close()
            return render_template('success.html',
                title='Classroom Added Successfully! 🏫',
                message=f'Classroom {nameclass} for course {course} has been created successfully.',
                action_type='classroom')
        except Error as e:
            print(f"Error: {e}")
            return "Error al agregar clase", 500
    return render_template('add_classroom.html',
            current_page='🏫 Add Classroom',
            current_route='add_classroom')

# Rutas para borrar registros
@app.route('/delete_student/<int:student_id>')
def delete_student(student_id):
    connection = get_db_connection()
    if connection is None:
        return "Error de conexión a la base de datos", 500
    
    try:
        cur = connection.cursor()
        cur.execute("DELETE FROM student WHERE id = %s", (student_id,))
        connection.commit()
        cur.close()
        connection.close()
        return render_template('success.html',
            title='Student Deleted Successfully! 🗑️',
            message=f'The student has been removed from the system.',
            action_type='student')
    except Error as e:
        print(f"Error: {e}")
        return "Error al eliminar estudiante", 500

@app.route('/delete_classroom/<int:classroom_id>')
def delete_classroom(classroom_id):
    connection = get_db_connection()
    if connection is None:
        return "Error de conexión a la base de datos", 500
    
    try:
        cur = connection.cursor()
        cur.execute("DELETE FROM classroom WHERE id = %s", (classroom_id,))
        connection.commit()
        cur.close()
        connection.close()
        return render_template('success.html',
            title='Classroom Deleted Successfully! 🗑️',
            message=f'The classroom has been removed from the system.',
            action_type='classroom')
    except Error as e:
        print(f"Error: {e}")
        return "Error al eliminar clase", 500

# Rutas para editar registros
@app.route('/edit_student/<int:student_id>', methods=['GET', 'POST'])
def edit_student(student_id):
    connection = get_db_connection()
    if connection is None:
        return "Error de conexión a la base de datos", 500
    
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
            cur.close()
            connection.close()
            return render_template('success.html',
                title='Student Updated Successfully! ✏️',
                message=f'Student {name} {surname} has been updated successfully.',
                action_type='student')
        except Error as e:
            print(f"Error: {e}")
            return "Error al actualizar estudiante", 500
    
    # GET request - mostrar formulario con datos actuales
    try:
        cur = connection.cursor(dictionary=True)
        cur.execute("SELECT * FROM student WHERE id = %s", (student_id,))
        student = cur.fetchone()
        cur.close()
        connection.close()
        
        if student:
            return render_template('edit_student.html', 
                student=student,
                current_page=f'✏️ Edit Student: {student["name"]} {student["surname"]}',
                current_route='edit_student')
        else:
            return "Estudiante no encontrado", 404
    except Error as e:
        print(f"Error: {e}")
        return "Error al obtener datos del estudiante", 500

@app.route('/edit_classroom/<int:classroom_id>', methods=['GET', 'POST'])
def edit_classroom(classroom_id):
    connection = get_db_connection()
    if connection is None:
        return "Error de conexión a la base de datos", 500
    
    if request.method == 'POST':
        nameclass = request.form['nameclass']
        course = request.form['course']
        
        try:
            cur = connection.cursor()
            cur.execute("UPDATE classroom SET nameclass=%s, course=%s WHERE id=%s", 
                (nameclass, course, classroom_id))
            connection.commit()
            cur.close()
            connection.close()
            return render_template('success.html',
                title='Classroom Updated Successfully! ✏️',
                message=f'Classroom {nameclass} has been updated successfully.',
                action_type='classroom')
        except Error as e:
            print(f"Error: {e}")
            return "Error al actualizar clase", 500
    
    # GET request - mostrar formulario con datos actuales
    try:
        cur = connection.cursor(dictionary=True)
        cur.execute("SELECT * FROM classroom WHERE id = %s", (classroom_id,))
        classroom = cur.fetchone()
        cur.close()
        connection.close()
        
        if classroom:
            return render_template('edit_classroom.html', 
                classroom=classroom,
                current_page=f'✏️ Edit Classroom: {classroom["nameclass"]}',
                current_route='edit_classroom')
        else:
            return "Clase no encontrada", 404
    except Error as e:
        print(f"Error: {e}")
        return "Error al obtener datos de la clase", 500

def get_ecs_container_id():
    metadata_uri = os.environ.get('ECS_CONTAINER_METADATA_URI_V4') or os.environ.get('ECS_CONTAINER_METADATA_URI')
    
    if not metadata_uri:
        return "Error: No metadata URI"

    try:
        response = requests.get(metadata_uri, timeout=2)
        response.raise_for_status() # Lanza error si el status no es 200
        return response.json().get('DockerId')
    except Exception as e:
        return f"Error: {e}"

init_db() # Inicializar la base de datos al iniciar la aplicación

if __name__ == '__main__':
    import socket
    # Configuración segura del servidor usando variables de entorno
    host = os.getenv('FLASK_HOST', '0.0.0.0')
    port = int(os.getenv('FLASK_PORT', 80))
    debug = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    container_id = socket.gethostname()
    print(f"Starting Flask app in container: {container_id}")
    app.run(host=host, port=port, debug=debug)

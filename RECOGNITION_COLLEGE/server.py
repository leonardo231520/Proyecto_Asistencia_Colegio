from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
import os

app = Flask(__name__)
CORS(app)  # Permitir solicitudes desde el frontend

# Configuración de la base de datos
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'attendance_system'
}

# Conectar a la base de datos
def connect_db():
    return mysql.connector.connect(**db_config)

# Endpoint para registrar un docente
@app.route('/api/teachers', methods=['POST'])
def register_teacher():
    try:
        data = request.form
        first_name = data['first_name']
        last_name = data['last_name']
        email = data['email']
        photo = request.files['photo']

        # Guardar la foto
        photo_path = os.path.join('photos', f"{first_name}_{last_name}.jpg")
        photo.save(photo_path)

        # Insertar en la base de datos
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO teachers (first_name, last_name, email, photo_path) VALUES (%s, %s, %s, %s)",
            (first_name, last_name, email, photo_path)
        )
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({'message': 'Docente registrado correctamente'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Endpoint para obtener todos los docentes
@app.route('/api/teachers', methods=['GET'])
def get_teachers():
    try:
        conn = connect_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id, first_name, last_name, email, photo_path FROM teachers")
        teachers = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(teachers), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Endpoint para registrar asistencia
@app.route('/api/attendance', methods=['POST'])
def register_attendance():
    try:
        data = request.json
        teacher_id = data['teacher_id']
        entry = data.get('entry', True)

        conn = connect_db()
        cursor = conn.cursor()
        now = datetime.now()
        status = 'early' if now.time() < time(8, 0) else 'late'

        if entry:
            cursor.execute(
                "INSERT INTO attendance (teacher_id, entry_time, status) VALUES (%s, %s, %s)",
                (teacher_id, now, status)
            )
        else:
            cursor.execute(
                "UPDATE attendance SET exit_time = %s WHERE teacher_id = %s AND DATE(entry_time) = CURDATE()",
                (now, teacher_id)
            )

        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'message': 'Asistencia registrada correctamente'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Endpoint para obtener asistencias
@app.route('/api/attendance', methods=['GET'])
def get_attendance():
    try:
        conn = connect_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT a.id, t.first_name, t.last_name, a.entry_time, a.exit_time, a.status
            FROM attendance a
            JOIN teachers t ON a.teacher_id = t.id
        """)
        attendance = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(attendance), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
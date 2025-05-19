import face_recognition
import cv2
import numpy as np
import mysql.connector
from datetime import datetime, time

# Configuración de la base de datos
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'attendance_system'
}

# Función para conectar a la base de datos
def connect_db():
    return mysql.connector.connect(**db_config)

# Cargar imágenes de docentes desde la base de datos
def load_teachers():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, first_name, last_name, email, photo_path FROM teachers")
    teachers = cursor.fetchall()
    cursor.close()
    conn.close()
    
    known_face_encodings = []
    known_face_metadata = []
    
    for teacher in teachers:
        image = face_recognition.load_image_file(teacher[4])
        encoding = face_recognition.face_encodings(image)[0]
        known_face_encodings.append(encoding)
        known_face_metadata.append({
            'id': teacher[0],
            'first_name': teacher[1],
            'last_name': teacher[2],
            'email': teacher[3]
        })
    
    return known_face_encodings, known_face_metadata

# Registrar asistencia
def register_attendance(teacher_id, entry=True):
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

# Main: Reconocimiento facial
def main():
    known_face_encodings, known_face_metadata = load_teachers()
    video_capture = cv2.VideoCapture(0)  # Cámara predeterminada
    
    while True:
        ret, frame = video_capture.read()
        if not ret:
            break
        
        # Convertir la imagen de BGR (OpenCV) a RGB (face_recognition)
        rgb_frame = frame[:, :, ::-1]
        
        # Encontrar rostros y codificaciones
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
        
        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Desconocido"
            
            if True in matches:
                first_match_index = matches.index(True)
                metadata = known_face_metadata[first_match_index]
                name = f"{metadata['first_name']} {metadata['last_name']}"
                teacher_id = metadata['id']
                
                # Registrar entrada o salida (basado en hora o lógica específica)
                now = datetime.now()
                if now.time() < time(12, 0):  # Ejemplo: entrada antes de mediodía
                    register_attendance(teacher_id, entry=True)
                    print(f"Entrada registrada para {name}")
                else:
                    register_attendance(teacher_id, entry=False)
                    print(f"Salida registrada para {name}")
            
            # Mostrar nombre en la cámara
            for (top, right, bottom, left) in face_locations:
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
        
        cv2.imshow('Video', frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    video_capture.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
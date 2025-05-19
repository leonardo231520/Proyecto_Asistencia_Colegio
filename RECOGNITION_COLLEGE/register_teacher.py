import mysql.connector
import os
import cv2
import re

# Configuración de la base de datos
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',  # Cambia por tu contraseña
    'database': 'attendance_system'
}

# Carpeta para almacenar fotos
PHOTOS_DIR = 'photos'
if not os.path.exists(PHOTOS_DIR):
    os.makedirs(PHOTOS_DIR)

# Función para conectar a la base de datos
def connect_db():
    return mysql.connector.connect(**db_config)

# Validar correo electrónico
def is_valid_email(email):
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(pattern, email) is not None

# Capturar foto desde la cámara
def capture_photo(teacher_name):
    video_capture = cv2.VideoCapture(0)  # Cámara predeterminada
    if not video_capture.isOpened():
        print("Error: No se pudo abrir la cámara.")
        return None
    
    print("Presiona 's' para capturar la foto o 'q' para salir.")
    while True:
        ret, frame = video_capture.read()
        if not ret:
            print("Error: No se pudo leer el frame.")
            break
        
        cv2.imshow('Capturar Foto', frame)
        
        key = cv2.waitKey(1) & 0xFF
        if key == ord('s'):
            photo_path = os.path.join(PHOTOS_DIR, f"{teacher_name.replace(' ', '_')}.jpg")
            cv2.imwrite(photo_path, frame)
            print(f"Foto guardada en: {photo_path}")
            video_capture.release()
            cv2.destroyAllWindows()
            return photo_path
        elif key == ord('q'):
            break
    
    video_capture.release()
    cv2.destroyAllWindows()
    return None

# Registrar docente en la base de datos
def register_teacher(first_name, last_name, email, photo_path):
    try:
        conn = connect_db()
        cursor = conn.cursor()
        
        cursor.execute(
            "INSERT INTO teachers (first_name, last_name, email, photo_path) VALUES (%s, %s, %s, %s)",
            (first_name, last_name, email, photo_path)
        )
        
        conn.commit()
        print(f"Docente {first_name} {last_name} registrado correctamente.")
        
        cursor.close()
        conn.close()
    except mysql.connector.Error as err:
        print(f"Error al registrar docente: {err}")

# Main: Interfaz para registrar docentes
def main():
    while True:
        print("\n=== Registro de Docentes ===")
        first_name = input("Nombre del docente: ").strip().capitalize()
        if not first_name:
            print("El nombre no puede estar vacío.")
            continue
        
        last_name = input("Apellido del docente: ").strip().capitalize()
        if not last_name:
            print("El apellido no puede estar vacío.")
            continue
        
        email = input("Correo electrónico: ").strip().lower()
        if not is_valid_email(email):
            print("Correo electrónico no válido.")
            continue
        
        print("¿Deseas capturar una foto con la cámara? (s/n)")
        capture_choice = input().strip().lower()
        
        photo_path = None
        if capture_choice == 's':
            photo_path = capture_photo(f"{first_name}_{last_name}")
            if not photo_path:
                print("No se capturó ninguna foto. Intenta de nuevo.")
                continue
        else:
            photo_input = input("Ruta de la foto (ejemplo: photos/juan.jpg): ").strip()
            if os.path.exists(photo_input) and photo_input.lower().endswith(('.jpg', '.jpeg', '.png')):
                photo_path = photo_input
            else:
                print("La ruta de la foto no es válida o el archivo no existe.")
                continue
        
        # Registrar en la base de datos
        register_teacher(first_name, last_name, email, photo_path)
        
        print("¿Deseas registrar otro docente? (s/n)")
        if input().strip().lower() != 's':
            break

if __name__ == "__main__":
    main()
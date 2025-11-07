# /backend_mongo/app.py
from flask import Flask, jsonify, request
from pymongo import MongoClient
from dotenv import load_dotenv
from flask_cors import CORS # Para resolver el problema de comunicación con el frontend
import os

# Cargar variables de entorno (incluyendo la URI de Mongo)
load_dotenv()

# --- Configuración de Flask y MongoDB ---
app = Flask(__name__)
CORS(app) # Habilitar CORS para todas las rutas

# Conexión a MongoDB
MONGO_URI = os.getenv('MONGO_URI')
MONGO_DATABASE = os.getenv('MONGO_DATABASE')

try:
    client = MongoClient(MONGO_URI)
    db = client[MONGO_DATABASE]
    habilidades_collection = db.habilidades # La colección se llamará 'habilidades'
    print(f"Conexión exitosa a MongoDB: {MONGO_DATABASE}")
except Exception as e:
    print(f"Error al conectar a MongoDB: {e}")
    habilidades_collection = None # Manejo de error si la conexión falla

# --- Inicialización de Datos Iniciales ---
def init_data():
    if habilidades_collection is None:
        return

    # Datos iniciales basados en tu frontend
    habilidades_iniciales = [
        {"nombre": "Trabajo en Equipo", "icono": "🤝", "descripcion": "Colaborar eficientemente con otros."},
        {"nombre": "Adaptabilidad al Cambio", "icono": "🔄", "descripcion": "Responder positivamente a nuevas situaciones."},
        {"nombre": "Aprendizaje Continuo", "icono": "📚", "descripcion": "Proactividad en la adquisición de nuevos conocimientos."},
        {"nombre": "Comunicación Efectiva", "icono": "💬", "descripcion": "Transmitir ideas de forma clara y concisa."},
        {"nombre": "Respeto", "icono": "🤗", "descripcion": "Valoración de la diversidad y las ideas ajenas."},
        {"nombre": "Creatividad e Innovación", "icono": "💡", "descripcion": "Generar ideas originales y soluciones novedosas."},
        {"nombre": "Proactividad", "icono": "⚡", "descripcion": "Tomar la iniciativa para mejorar procesos."},
        {"nombre": "Gestión del Tiempo", "icono": "⏰", "descripcion": "Organizar y planificar tareas para la eficiencia."}
    ]

    # Insertar solo si la colección está vacía
    if habilidades_collection.count_documents({}) == 0:
        print("Insertando datos iniciales en MongoDB...")
        habilidades_collection.insert_many(habilidades_iniciales)
        print(f"{len(habilidades_iniciales)} habilidades insertadas.")
    else:
        print("La colección de habilidades ya contiene datos.")

# --- Rutas de la API (Endpoints) ---

# Ruta GET para obtener todas las habilidades
@app.route('/api/habilidades', methods=['GET'])
def get_habilidades():
    if habilidades_collection is None:
        return jsonify({"message": "Error de conexión a la base de datos"}), 500

    # Busca todos los documentos
    habilidades = list(habilidades_collection.find())
    
    # PyMongo devuelve un campo '_id' de tipo ObjectId, que no es serializable a JSON.
    # Debemos convertirlo a string antes de enviarlo.
    for h in habilidades:
        h['_id'] = str(h['_id']) 
        
    return jsonify(habilidades)

# Ruta POST para agregar una nueva habilidad (Opcional)
@app.route('/api/habilidades', methods=['POST'])
def add_habilidad():
    if habilidades_collection is None:
        return jsonify({"message": "Error de conexión a la base de datos"}), 500
        
    data = request.get_json()
    
    if not all(k in data for k in ('nombre', 'icono')):
        return jsonify({"message": "Faltan campos requeridos (nombre, icono)"}), 400

    resultado = habilidades_collection.insert_one(data)
    
    # Devuelve el documento insertado (con el _id convertido a string)
    data['_id'] = str(resultado.inserted_id)
    return jsonify(data), 201

# --- Ejecución del Servidor ---
if __name__ == '__main__':
    # Inicializa los datos al inicio (solo si la colección está vacía)
    init_data() 
    
    PORT = 5000
    print(f"El backend está listo para servir datos en http://127.0.0.1:{PORT}/api/habilidades")
    app.run(debug=True, port=PORT)
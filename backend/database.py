from pymongo import MongoClient
import os

# 🔹 Conexión a MongoDB Atlas (cambia tu URI)
MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://TU_USUARIO:TU_CONTRASEÑA@cluster0.xxxxx.mongodb.net/")
client = MongoClient(MONGO_URI)

# Base de datos
db = client["softskills_db"]

# Colecciones
usuarios_collection = db["usuarios"]
encuestas_collection = db["encuestas"]

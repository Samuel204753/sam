from fastapi import APIRouter, HTTPException, status
from models import UsuarioRegistro, UsuarioLogin
from database import usuarios_collection
from jose import jwt
import bcrypt
import os

router = APIRouter(prefix="/auth", tags=["Autenticación"])

SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey")
ALGORITHM = "HS256"

# 🔹 Registro de usuario
@router.post("/register")
def register(usuario: UsuarioRegistro):
    if usuarios_collection.find_one({"email": usuario.email}):
        raise HTTPException(status_code=400, detail="El email ya está registrado")

    hashed_pw = bcrypt.hashpw(usuario.password.encode('utf-8'), bcrypt.gensalt())
    nuevo_usuario = {
        "nombre": usuario.nombre,
        "email": usuario.email,
        "password": hashed_pw
    }
    usuarios_collection.insert_one(nuevo_usuario)
    return {"mensaje": "Usuario registrado correctamente"}

# 🔹 Login de usuario
@router.post("/login")
def login(usuario: UsuarioLogin):
    user = usuarios_collection.find_one({"email": usuario.email})
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    if not bcrypt.checkpw(usuario.password.encode('utf-8'), user["password"]):
        raise HTTPException(status_code=401, detail="Contraseña incorrecta")

    token = jwt.encode({"usuario_id": str(user["_id"])}, SECRET_KEY, algorithm=ALGORITHM)
    return {"mensaje": "Inicio de sesión exitoso", "token": token, "nombre": user["nombre"]}

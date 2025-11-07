from pydantic import BaseModel, EmailStr
from typing import Optional

class UsuarioRegistro(BaseModel):
    nombre: str
    email: EmailStr
    password: str

class UsuarioLogin(BaseModel):
    email: EmailStr
    password: str

class Encuesta(BaseModel):
    usuario_id: str
    comunicacion: int
    liderazgo: int
    trabajo_en_equipo: int
    adaptabilidad: int

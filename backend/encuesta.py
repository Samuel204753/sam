from fastapi import APIRouter, HTTPException
from models import Encuesta
from database import encuestas_collection

router = APIRouter(prefix="/encuestas", tags=["Encuestas"])

@router.post("/")
def crear_encuesta(encuesta: Encuesta):
    encuestas_collection.insert_one(encuesta.dict())
    return {"mensaje": "Encuesta guardada correctamente"}

@router.get("/{usuario_id}")
def obtener_encuestas(usuario_id: str):
    datos = list(encuestas_collection.find({"usuario_id": usuario_id}, {"_id": 0}))
    if not datos:
        raise HTTPException(status_code=404, detail="No hay encuestas para este usuario")
    return datos

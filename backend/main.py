from fastapi import FastAPI
from auth import router as auth_router
from encuesta import router as encuesta_router

app = FastAPI(
    title="API de Habilidades Blandas",
    description="Backend con login, registro y encuesta de habilidades blandas",
    version="1.0"
)

app.include_router(auth_router)
app.include_router(encuesta_router)

@app.get("/")
def home():
    return {"mensaje": "API SoftSkills funcionando correctamente 🚀"}

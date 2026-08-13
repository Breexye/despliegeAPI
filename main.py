import os
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()


app = FastAPI(
    title="API de Currículum Profesional",
    description="API RESTful conectada a Supabase con Frontend integrado.",
    version="3.0.0"
)

# Servir archivos estáticos del frontend
app.mount("/static", StaticFiles(directory="frontend"), name="static")

# Conexión a Supabase
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase: Client = None
if SUPABASE_URL and SUPABASE_KEY:
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# Función auxiliar para obtener el JSON completo desde Supabase
def get_cv_data():
    if not supabase:
        raise HTTPException(status_code=500, detail="Supabase no configurado. Faltan variables de entorno.")
    response = supabase.table("curriculum").select("data").eq("id", 1).execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="CV no encontrado en base de datos")
    return response.data[0]["data"]

def update_cv_data(new_data):
    if not supabase:
        raise HTTPException(status_code=500, detail="Supabase no configurado. Faltan variables de entorno.")
    supabase.table("curriculum").update({"data": new_data}).eq("id", 1).execute()

# --- MODELOS PYDANTIC ---
class EducacionItem(BaseModel):
    institucion: str
    periodo: str
    titulo: str

class ProyectoItem(BaseModel):
    nombre: str
    periodo: str
    detalles: List[str]

class PersonalItem(BaseModel):
    nombre: str

# --- ENDPOINTS ---

@app.get("/", tags=["Inicio"])
def home():
    # Enviar el frontend al entrar a la raíz
    return FileResponse("frontend/index.html")

# 1. READ: Obtener todo el currículum
@app.get("/cv", tags=["CV Completo"])
def obtener_cv():
    return get_cv_data()

# --- CRUD EDUCACIÓN ---

@app.get("/cv/educacion", tags=["Educación"])
def obtener_educacion():
    data = get_cv_data()
    return data.get("educacion", [])

@app.post("/cv/educacion", tags=["Educación"])
def agregar_educacion(edu: EducacionItem):
    data = get_cv_data()
    data["educacion"].append(edu.model_dump())
    update_cv_data(data)
    return {"mensaje": "Educación agregada exitosamente", "educacion": data["educacion"]}

@app.delete("/cv/educacion/{institucion}", tags=["Educación"])
def eliminar_educacion(institucion: str):
    data = get_cv_data()
    educacion_filtrada = [e for e in data["educacion"] if e["institucion"].lower() != institucion.lower()]
    if len(educacion_filtrada) == len(data["educacion"]):
        raise HTTPException(status_code=404, detail="Institución no encontrada")
    data["educacion"] = educacion_filtrada
    update_cv_data(data)
    return {"mensaje": f"Educación de '{institucion}' eliminada correctamente"}

# --- CRUD PROYECTOS ---

@app.get("/cv/proyectos", tags=["Proyectos"])
def obtener_proyectos():
    data = get_cv_data()
    return data.get("proyectos", [])

@app.post("/cv/proyectos", tags=["Proyectos"])
def agregar_proyecto(proyecto: ProyectoItem):
    data = get_cv_data()
    data["proyectos"].append(proyecto.model_dump())
    update_cv_data(data)
    return {"mensaje": "Proyecto agregado exitosamente", "proyectos": data["proyectos"]}

@app.delete("/cv/proyectos/{nombre_proyecto}", tags=["Proyectos"])
def eliminar_proyecto(nombre_proyecto: str):
    data = get_cv_data()
    proyectos_filtrados = [p for p in data["proyectos"] if p["nombre"].lower() != nombre_proyecto.lower()]
    if len(proyectos_filtrados) == len(data["proyectos"]):
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")
    data["proyectos"] = proyectos_filtrados
    update_cv_data(data)
    return {"mensaje": f"Proyecto '{nombre_proyecto}' eliminado correctamente"}

# --- CRUD PERSONAL (PUT) ---
@app.put("/cv/personal", tags=["Personal"])
def actualizar_personal(personal: PersonalItem):
    data = get_cv_data()
    data["informacion_personal"]["nombre"] = personal.nombre
    update_cv_data(data)
    return {"mensaje": "Información personal actualizada exitosamente", "personal": data["informacion_personal"]}
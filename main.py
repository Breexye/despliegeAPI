import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from supabase import create_client, Client

app = FastAPI(
    title="API de Currículum con Supabase",
    description="API RESTful conectada a Supabase para gestionar el perfil profesional.",
    version="2.0.0"
)

# --- CONFIGURACIÓN DE SUPABASE ---
# Estas variables se leerán de las Environment Variables en Vercel (o de tu entorno local)
SUPABASE_URL = os.environ.get("https://abxaooaopkulsaepioih.supabase.co")
SUPABASE_KEY = os.environ.get("sb_publishable_gcV6ao5r1iAA_tbyu-IdkQ_OEvZwSqM")

if not SUPABASE_URL or not SUPABASE_KEY:
    # Esto ayuda a prevenir errores si no configuras las variables localmente
    supabase = None
else:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def verificar_conexion():
    if not supabase:
        raise HTTPException(
            status_code=500, 
            detail="Faltan las variables de entorno de Supabase (SUPABASE_URL o SUPABASE_KEY)."
        )

# --- MODELOS PYDANTIC ---
class EducacionItem(BaseModel):
    institucion: str
    periodo: str
    titulo: str

class ProyectoItem(BaseModel):
    nombre: str
    periodo: str
    detalles: List[str]


# --- ENDPOINTS DEL CRUD (Conectados a Supabase) ---

# 1. READ: Obtener toda la educación
@app.get("/cv/educacion", tags=["Educación"])
def obtener_educacion():
    verificar_conexion()
    response = supabase.table("educacion").select("*").execute()
    return response.data

# 2. CREATE: Agregar educación
@app.post("/cv/educacion", tags=["Educación"])
def agregar_educacion(edu: EducacionItem):
    verificar_conexion()
    response = supabase.table("educacion").insert(edu.model_dump()).execute()
    return {"mensaje": "Educación agregada correctamente", "data": response.data}

# 3. DELETE: Eliminar educación por institución
@app.delete("/cv/educacion/{institucion}", tags=["Educación"])
def eliminar_educacion(institucion: str):
    verificar_conexion()
    # Buscamos y eliminamos por el campo 'institucion'
    response = supabase.table("educacion").delete().eq("institucion", institucion).execute()
    
    if not response.data:
        raise HTTPException(status_code=404, detail="Institución no encontrada en la base de datos")
    
    return {"mensaje": f"Educación de '{institucion}' eliminada correctamente"}


# 4. READ: Obtener todos los proyectos
@app.get("/cv/proyectos", tags=["Proyectos"])
def obtener_proyectos():
    verificar_conexion()
    response = supabase.table("proyectos").select("*").execute()
    return response.data

# 5. CREATE: Agregar proyecto
@app.post("/cv/proyectos", tags=["Proyectos"])
def agregar_proyecto(proyecto: ProyectoItem):
    verificar_conexion()
    response = supabase.table("proyectos").insert(proyecto.model_dump()).execute()
    return {"mensaje": "Proyecto agregado correctamente", "data": response.data}

# 6. DELETE: Eliminar proyecto por nombre
@app.delete("/cv/proyectos/{nombre_proyecto}", tags=["Proyectos"])
def eliminar_proyecto(nombre_proyecto: str):
    verificar_conexion()
    response = supabase.table("proyectos").delete().eq("nombre", nombre_proyecto).execute()
    
    if not response.data:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado en la base de datos")
    
    return {"mensaje": f"Proyecto '{nombre_proyecto}' eliminado correctamente"}
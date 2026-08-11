from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI(
    title="API de Currículum Profesional",
    description="API RESTful basada en estructura JSON interna con soporte CRUD completo.",
    version="2.2.0"
)

# --- TU JSON DECLARADO ---
cv_data = {
    "informacion_personal": {
        "nombre": "Brenda Maria Chavez Diaz",
        "profesion": "TSU. DESARROLLO SOFTWARE",
        "contacto": {
            "email": "brenda15mariach@gmail.com",
            "telefono": "614-313-3114",
            "github": "github.com/Breexye"
        },
        "sobre_mi": "Soy una persona que le gusta la tecnología, con una actitud colaborativa y orientación al trabajo en equipo. Disfruto apoyar a mis compañeros, compartir conocimientos y contribuir al crecimiento colectivo."
    },
    "educacion": [
        {
            "institucion": "CBTIS 122",
            "periodo": "2016-2019",
            "titulo": "Tecnico en Programación"
        },
        {
            "institucion": "UTCH BIS",
            "periodo": "2024-Actualidad",
            "titulo": "TSU. Desarrollo Software / ING. Tecnologias de la informacion"
        }
    ],
    "idiomas": [
        "Español - Nativo",
        "Inglés - Conversacional",
        "LSM - Basico"
    ],
    "certificaciones": [
        "Basic SolidWorks",
        "Microsoft Office Suite"
    ],
    "lenguajes_y_frameworks": [
        "Python", "C#", "Java (Basico)", "ReactNative (Basico)", "MySQL", "CSS", "HTML", "PostgreSQL"
    ],
    "proyectos": [
        {
            "nombre": "CHAMBAPP",
            "periodo": "Septiembre 2025 - Actualidad",
            "detalles": [
                "Diseño de Front",
                "Manejo de Bases de datos y Querys",
                "Funciones de validación",
                "QA tester"
            ]
        },
        {
            "nombre": "Hackaton Reto Marte 2026",
            "periodo": "Marzo 2026 - Mayo 2026",
            "detalles": [
                "Representación nivel estatal",
                "Colaboración en equipos multidisciplinarios",
                "Investigación científica",
                "Biotransformación de tierra",
                "Oratoria"
            ]
        },
        {
            "nombre": "Prueba de Proyecto2",
            "periodo": "2026",
            "detalles": [
                "Detalle 1",
                "Detalle 2"
            ]
        }
    ]
}

# --- MODELOS PYDANTIC ---
class EducacionItem(BaseModel):
    institucion: str
    periodo: str
    titulo: str

class ProyectoItem(BaseModel):
    nombre: str
    periodo: str
    detalles: List[str]


# --- ENDPOINTS ---

@app.get("/", tags=["Inicio"])
def home():
    return {
        "mensaje": "¡Bienvenido a mi API de Currículum!",
        "documentacion": "/docs",
        "ver_cv": "/cv"
    }

# 1. READ: Obtener todo el currículum
@app.get("/cv", tags=["CV Completo"])
def obtener_cv():
    return cv_data

# --- CRUD EDUCACIÓN ---

@app.get("/cv/educacion", tags=["Educación"])
def obtener_educacion():
    return cv_data["educacion"]

@app.post("/cv/educacion", tags=["Educación"])
def agregar_educacion(edu: EducacionItem):
    cv_data["educacion"].append(edu.model_dump())
    return {"mensaje": "Educación agregada exitosamente", "educacion": cv_data["educacion"]}

@app.delete("/cv/educacion/{institucion}", tags=["Educación"])
def eliminar_educacion(institucion: str):
    global cv_data
    educacion_filtrada = [e for e in cv_data["educacion"] if e["institucion"].lower() != institucion.lower()]
    if len(educacion_filtrada) == len(cv_data["educacion"]):
        raise HTTPException(status_code=404, detail="Institución no encontrada")
    cv_data["educacion"] = educacion_filtrada
    return {"mensaje": f"Educación de '{institucion}' eliminada correctamente"}


# --- CRUD PROYECTOS ---

@app.get("/cv/proyectos", tags=["Proyectos"])
def obtener_proyectos():
    return cv_data["proyectos"]

@app.post("/cv/proyectos", tags=["Proyectos"])
def agregar_proyecto(proyecto: ProyectoItem):
    cv_data["proyectos"].append(proyecto.model_dump())
    return {"mensaje": "Proyecto agregado exitosamente", "proyectos": cv_data["proyectos"]}

@app.delete("/cv/proyectos/{nombre_proyecto}", tags=["Proyectos"])
def eliminar_proyecto(nombre_proyecto: str):
    global cv_data
    proyectos_filtrados = [p for p in cv_data["proyectos"] if p["nombre"].lower() != nombre_proyecto.lower()]
    if len(proyectos_filtrados) == len(cv_data["proyectos"]):
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")
    cv_data["proyectos"] = proyectos_filtrados
    return {"mensaje": f"Proyecto '{nombre_proyecto}' eliminado correctamente"}
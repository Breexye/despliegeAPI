import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

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

try:
    print("Intentando insertar datos iniciales en Supabase...")
    # Verificar si existe o insertar
    response = supabase.table("curriculum").upsert({"id": 1, "data": cv_data}).execute()
    print("Éxito:", response.data)
except Exception as e:
    print("Error:", e)

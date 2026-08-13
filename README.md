# API de Currículum Profesional - Despliegue

Esta API RESTful proporciona un currículum interactivo consumiendo datos desde Supabase y cuenta con una interfaz web (frontend) integrada.

## URL Pública (Producción)
**URL de la API:** `https://despliege-api.vercel.app/`

## Configuración y Variables de Entorno

### Configuración de la Base de Datos (Supabase)
Para que la API funcione correctamente, es necesario ejecutar el siguiente script SQL en el editor de SQL de Supabase para crear la tabla necesaria:

```sql
CREATE TABLE curriculum (
  id integer primary key,
  data jsonb
);
```

### Variables de Entorno
En tu entorno de producción (Vercel) y entorno local (`.env`), debes configurar las siguientes variables:
- `SUPABASE_URL`: URL de tu proyecto de Supabase.
- `SUPABASE_KEY`: Llave de API (anon/public) de Supabase.

### Dependencias
El proyecto utiliza Python y FastAPI. Las dependencias principales (listadas en `requirements.txt`) son:
- `fastapi`
- `uvicorn`
- `pydantic`
- `supabase`
- `python-dotenv`

---

## Proceso de Despliegue (Vercel)

1. **Preparación del Entorno:** Se separó el código backend (FastAPI) del frontend (archivos estáticos dentro de la carpeta `/frontend`), creando una estructura más limpia.
2. **Configuración de Vercel:** Se creó el archivo `vercel.json` configurando `@vercel/python` para el manejo de Serverless Functions y apuntando todo el tráfico a `main.py`.
3. **Variables de Entorno en Vercel:** Se añadieron `SUPABASE_URL` y `SUPABASE_KEY` en los *Settings > Environment Variables* de Vercel para conectar producción a Supabase sin exponer credenciales.
4. **Deploy:** El proyecto se enlaza desde GitHub hacia Vercel, el cual realiza el *build* e instala automáticamente las dependencias del `requirements.txt`.

### Problemas encontrados y solucionados durante el despliegue

1. **Error de sintaxis en archivo de Vercel (Página en blanco):**
   - **Problema:** Vercel no reconocía el proyecto de Python y mostraba la página en blanco o como un directorio, ya que el archivo de configuración tenía un error tipográfico (`versel.json`).
   - **Solución:** Se renombró el archivo a `vercel.json` y se ajustaron las reglas de `routes` para que toda petición `/.*` se redirija correctamente a `main.py`.

2. **Migración a Base de Datos (Supabase):**
   - **Problema:** Mantener el JSON en memoria (`cv_data`) implicaba que cualquier POST o DELETE se borraba al reiniciar el servidor en Vercel, ya que los Serverless Functions son "stateless" (sin estado).
   - **Solución:** Se migró el almacenamiento a Supabase. Se implementó una tabla `curriculum` con una columna JSONB, y se actualizaron todos los endpoints de FastAPI para usar la librería `supabase-py`. De este modo, los cambios son persistentes.

---

## Instrucciones para consumir la API (Endpoints)

La API cuenta con una interfaz web en la ruta raíz (`/`) desde donde puedes hacer pruebas fácilmente, y también soporta los siguientes endpoints para ser consumidos mediante Postman o Fetch:

### 1. Obtener Currículum Completo (GET)
- **Endpoint:** `GET /cv`
- **Descripción:** Retorna el JSON completo con información personal, educación, habilidades y proyectos.

### 2. Obtener Educación (GET)
- **Endpoint:** `GET /cv/educacion`
- **Descripción:** Devuelve un arreglo con el historial educativo.

### 3. Agregar un Proyecto (POST)
- **Endpoint:** `POST /cv/proyectos`
- **Body (JSON):**
  ```json
  {
    "nombre": "Mi Nuevo Proyecto",
    "periodo": "2026",
    "detalles": ["Desarrollo Backend", "Supabase"]
  }
  ```
- **Descripción:** Agrega un nuevo proyecto al portafolio.

### 4. Actualizar Información Personal (PUT)
- **Endpoint:** `PUT /cv/personal`
- **Body (JSON):**
  ```json
  {
    "nombre": "Nuevo Nombre Completo"
  }
  ```
- **Descripción:** Actualiza el nombre del perfil.

### 5. Eliminar un Proyecto (DELETE)
- **Endpoint:** `DELETE /cv/proyectos/{nombre_proyecto}`
- **Ejemplo:** `DELETE /cv/proyectos/CHAMBAPP`
- **Descripción:** Elimina un proyecto existente buscando por su nombre exacto. Si no existe, retorna error `404`.

### Prueba de Error (404 Not Found)
- **Endpoint:** `GET /ruta-inexistente` o `DELETE /cv/proyectos/ProyectoInventado`
- **Resultado:** Retornará un error `404 Not Found`, confirmando el correcto manejo de errores de la API.
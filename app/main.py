import os
import psycopg
from fastapi import FastAPI, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

aplicacion = FastAPI()
plantillas = Jinja2Templates(directory="app/templates")

def conectar():
    return psycopg.connect(
        host=os.environ["DB_HOST"],
        dbname=os.environ["DB_NAME"],
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
    )

def crear_tabla():
    with conectar() as conexion, conexion.cursor() as cursor:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tareas (
                id SERIAL PRIMARY KEY,
                titulo TEXT NOT NULL,
                hecha BOOLEAN NOT NULL DEFAULT FALSE,
                creada TIMESTAMPTZ NOT NULL DEFAULT now()
            )
        """)

crear_tabla()

@aplicacion.get("/")
def inicio(peticion: Request):
    with conectar() as conexion, conexion.cursor() as cursor:
        cursor.execute("SELECT id, titulo, hecha FROM tareas ORDER BY creada DESC")
        tareas = cursor.fetchall()
    return plantillas.TemplateResponse(
        peticion,
        "index.html",
        {"titulo": "Mini-Oficina", "tareas": tareas}
    )

@aplicacion.post("/tareas")
def crear_tarea(titulo: str = Form(...)):
    with conectar() as conexion, conexion.cursor() as cursor:
        cursor.execute("INSERT INTO tareas (titulo) VALUES (%s)", (titulo,))
    return RedirectResponse("/", status_code=303)

@aplicacion.get("/healthz")
def salud():
    with conectar() as conexion, conexion.cursor() as cursor:
        cursor.execute("SELECT 1")
        cursor.fetchone()
    return {"estado": "ok", "base_de_datos": "ok"}
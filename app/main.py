import os
import psycopg
from fastapi import FastAPI, Request
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

@aplicacion.get("/")
def inicio(peticion: Request):
    return plantillas.TemplateResponse(peticion, "index.html", {"titulo": "Mini-Oficina"})

@aplicacion.get("/healthz")
def salud():
    with conectar() as conexion, conexion.cursor() as cursor:
        cursor.execute("SELECT 1")
        cursor.fetchone()
    return {"estado": "ok", "base_de_datos": "ok"}

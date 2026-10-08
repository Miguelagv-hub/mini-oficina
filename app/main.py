from fastapi import Depends, FastAPI, Request
from fastapi.templating import Jinja2Templates
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.db import Base, engine, obtener_db
import app.models  # Asegura que SQLAlchemy cargue la definición de las tablas

# Crea las tablas en PostgreSQL si aún no existen
Base.metadata.create_all(bind=engine)

aplicacion = FastAPI()

plantillas = Jinja2Templates(directory="app/templates")


@aplicacion.get("/")
def inicio(peticion: Request):
    """La pagina principal: http://localhost:8000"""
    return plantillas.TemplateResponse(peticion, "index.html", {"titulo": "Mini-Oficina"})


@aplicacion.get("/healthz")
def salud():
    return {"estado": "ok"}


@aplicacion.get("/db-status")
def estado_db(db: Session = Depends(obtener_db)):
    """Comprueba la conexion real con PostgreSQL ejecutando SELECT 1"""
    db.execute(text("SELECT 1"))
    return {"database": "conectada y lista"}
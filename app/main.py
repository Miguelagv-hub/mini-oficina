from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates

aplicacion = FastAPI()

plantillas = Jinja2Templates(directory="app/templates")


@aplicacion.get("/")
def inicio(peticion: Request):
    """La pagina principal: http://localhost:8000"""
    return plantillas.TemplateResponse(peticion, "index.html", {"titulo": "Mini-Oficina"})


@aplicacion.get("/healthz")
def salud():
    return {"estado": "ok"}
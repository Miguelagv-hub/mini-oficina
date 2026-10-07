"""La Mini-Oficina: punto de entrada de la aplicacion."""
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates

aplicacion = FastAPI()
plantillas = Jinja2Templates(directory="app/templates")

@aplicacion.get("/")
def inicio(peticion: Request):
    """La pagina principal: http://localhost:8000"""
    return plantillas.TemplateResponse(
        request=peticion,
        name="index.html",
        context={"titulo": "Mini-Oficina"}
    )
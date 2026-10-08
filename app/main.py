from fastapi import Depends, FastAPI, HTTPException, Request, status
from fastapi.templating import Jinja2Templates
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.db import Base, engine, obtener_db
import app.models as models
import app.schemas as schemas

Base.metadata.create_all(bind=engine)

aplicacion = FastAPI()

plantillas = Jinja2Templates(directory="app/templates")


@aplicacion.get("/")
def inicio(peticion: Request):
    return plantillas.TemplateResponse(peticion, "index.html", {"titulo": "Mini-Oficina"})


@aplicacion.get("/healthz")
def salud():
    return {"estado": "ok"}


@aplicacion.get("/db-status")
def estado_db(db: Session = Depends(obtener_db)):
    db.execute(text("SELECT 1"))
    return {"database": "conectada y lista"}


# --- CRUD DOCUMENTOS ---

@aplicacion.post("/api/documentos", response_model=schemas.DocumentoRespuesta, status_code=status.HTTP_201_CREATED)
def crear_documento(doc: schemas.DocumentoCrear, db: Session = Depends(obtener_db)):
    nuevo_doc = models.Documento(
        titulo=doc.titulo,
        contenido=doc.contenido,
        categoria=doc.categoria
    )
    db.add(nuevo_doc)
    db.commit()
    db.refresh(nuevo_doc)
    return nuevo_doc


@aplicacion.get("/api/documentos", response_model=list[schemas.DocumentoRespuesta])
def listar_documentos(db: Session = Depends(obtener_db)):
    return db.query(models.Documento).all()


@aplicacion.get("/api/documentos/{doc_id}", response_model=schemas.DocumentoRespuesta)
def obtener_documento(doc_id: int, db: Session = Depends(obtener_db)):
    doc = db.query(models.Documento).filter(models.Documento.id == doc_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Documento no encontrado")
    return doc


@aplicacion.delete("/api/documentos/{doc_id}", status_code=status.HTTP_204_NO_CONTENT)
def borrar_documento(doc_id: int, db: Session = Depends(obtener_db)):
    doc = db.query(models.Documento).filter(models.Documento.id == doc_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Documento no encontrado")
    db.delete(doc)
    db.commit()
    return None
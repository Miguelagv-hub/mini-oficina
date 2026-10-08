from datetime import datetime
from pydantic import BaseModel, ConfigDict


class DocumentoBase(BaseModel):
    titulo: str
    contenido: str
    categoria: str = "general"


class DocumentoCrear(DocumentoBase):
    pass


class DocumentoRespuesta(DocumentoBase):
    id: int
    creado_en: datetime

    model_config = ConfigDict(from_attributes=True)
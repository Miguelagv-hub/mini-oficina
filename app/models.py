from datetime import datetime
from sqlalchemy import Column, DateTime, Integer, String, Text
from app.db import Base


class Documento(Base):
    __tablename__ = "documentos"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String(200), nullable=False)
    contenido = Column(Text, nullable=False)
    categoria = Column(String(50), default="general")
    creado_en = Column(DateTime, default=datetime.utcnow)
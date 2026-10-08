import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

db_user = os.getenv("DB_USER", "oficina")
db_password = os.getenv("DB_PASSWORD", "oficina")
db_host = os.getenv("DB_HOST", "db")
db_name = os.getenv("DB_NAME", "oficina")

DATABASE_URL = f"postgresql://{db_user}:{db_password}@{db_host}:5432/{db_name}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def obtener_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
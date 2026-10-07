# Imagen base: Python 3.12 en su version "slim" (mas ligera).
FROM python:3.12-slim

# Todo lo que pase dentro del contenedor ocurre en esta carpeta.
WORKDIR /app

# Primero las dependencias, solas: asi Docker se guarda este paso en cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Y ahora el codigo de la aplicacion.
COPY app/ ./app/

# El comando que arranca la aplicacion cuando el contenedor se enciende.
CMD ["uvicorn", "app.main:aplicacion", "--host", "0.0.0.0", "--port", "8000", "--reload"]
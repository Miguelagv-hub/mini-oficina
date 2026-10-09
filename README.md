# Mini-Oficina

Aplicación web de gestión de tareas desarrollada con FastAPI, PostgreSQL y plantillas HTML (Jinja2). Su objetivo es simular una oficina real aplicando un flujo de trabajo profesional con ramas y Pull Requests mediante Docker.

## Requisitos previos

- **Docker** y **Docker Compose** instalados en tu equipo.

## Estructura de carpetas

- `app/`: Contiene la lógica backend y las vistas de la aplicación.
  - `main.py`: Rutas, endpoints de FastAPI y conexión a la base de datos.
  - `templates/`: Ficheros HTML con plantillas Jinja2.
- `Dockerfile`: Receta para empaquetar la aplicación web en Python.
- `docker-compose.yml`: Orquestador que levanta la base de datos PostgreSQL y la web conjuntamente.
- `requirements.txt`: Librerías y dependencias fijadas del proyecto.

## Cómo levantarlo desde cero

1. Clona el repositorio en tu ordenador y entra en su directorio:

   git clone <url-de-tu-repositorio>
   cd mini-oficina
   Crea tu archivo de configuración de entorno local:

cp dotenv.example .env
Construye y arranca los contenedores en segundo plano:

docker compose up -d --build
Abre en tu navegador para comprobar que funciona:

Aplicación: http://localhost:8000

Healthcheck: http://localhost:8000/healthz

Cómo pararlo
Apagar manteniendo los datos guardados en el volumen de la base de datos:


docker compose down
Apagar y borrar completamente los datos (empezar de cero):

docker compose down -v
import os
import psycopg
from fastapi import FastAPI, Request, Form
from fastapi.responses import RedirectResponse
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

def crear_tabla():
    with conectar() as conexion, conexion.cursor() as cursor:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tareas (
                id SERIAL PRIMARY KEY,
                titulo TEXT NOT NULL,
                hecha BOOLEAN NOT NULL DEFAULT FALSE,
                creada TIMESTAMPTZ NOT NULL DEFAULT now()
            )
        """)

crear_tabla()

@aplicacion.get("/")
def inicio(peticion: Request):
    with conectar() as conexion, conexion.cursor() as cursor:
        cursor.execute("SELECT id, titulo, hecha FROM tareas ORDER BY creada DESC")
        tareas = cursor.fetchall()
    
    # Lógica del contador exigida por el tutor
    total = len(tareas)
    pendientes = sum(1 for tarea in tareas if not tarea[2])

    return plantillas.TemplateResponse(
        peticion,
        "index.html",
        {
            "titulo": "Mini-Oficina",
            "tareas": tareas,
            "total": total,
            "pendientes": pendientes
        }
    )

@aplicacion.post("/tareas")
def crear_tarea(titulo: str = Form(...)):
    with conectar() as conexion, conexion.cursor() as cursor:
        cursor.execute("INSERT INTO tareas (titulo) VALUES (%s)", (titulo,))
    return RedirectResponse("/", status_code=303)

@aplicacion.post("/tareas/{id_tarea}/hecha")
def marcar_hecha(id_tarea: int):
    with conectar() as conexion, conexion.cursor() as cursor:
        cursor.execute("UPDATE tareas SET hecha = TRUE WHERE id = %s", (id_tarea,))
    return RedirectResponse("/", status_code=303)

@aplicacion.post("/tareas/{id_tarea}/borrar")
def borrar_tarea(id_tarea: int):
    with conectar() as conexion, conexion.cursor() as cursor:
        cursor.execute("DELETE FROM tareas WHERE id = %s", (id_tarea,))
    return RedirectResponse("/", status_code=303)

@aplicacion.get("/healthz")
def salud():
    with conectar() as conexion, conexion.cursor() as cursor:
        cursor.execute("SELECT 1")
        cursor.fetchone()
    return {"estado": "ok", "base_de_datos": "ok"}
```[cite: 27]

---

### 3. Actualiza `app/templates/index.html`
Copia este código y guárdalo en **`app/templates/index.html`**. Añade el contador visible en pantalla justo debajo del formulario[cite: 12, 27]:

```html
<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{{ titulo }}</title>
  <style>
    body { font-family: system-ui, sans-serif; max-width: 640px; margin: 40px auto; padding: 0 16px; color: #1c2733; }
    h1 { color: #0379B5; }
    form { display: flex; gap: 8px; margin-bottom: 12px; }
    input[type="text"] { flex: 1; padding: 8px 12px; border: 1px solid #ccc; border-radius: 4px; }
    button { padding: 8px 16px; background-color: #0379B5; color: white; border: none; border-radius: 4px; cursor: pointer; }
    .contador { font-size: 14px; color: #555; margin-bottom: 24px; font-weight: bold; }
    ul { list-style: none; padding: 0; }
    li { display: flex; justify-content: space-between; align-items: center; padding: 8px 0; border-bottom: 1px solid #e1e4e8; }
    .acciones { display: flex; gap: 6px; }
    .tachada { text-decoration: line-through; color: #888; }
    .btn-hecha { background-color: #2e9e5b; padding: 4px 8px; font-size: 12px; }
    .btn-borrar { background-color: #d9534f; padding: 4px 8px; font-size: 12px; }
  </style>
</head>
<body>
  <h1>{{ titulo }}</h1>
  
  <form method="post" action="/tareas">
    <input type="text" name="titulo" placeholder="Que hay que hacer..." required>
    <button type="submit">Anadir</button>
  </form>

  <div class="contador">
    {{ pendientes }} pendientes de {{ total }}
  </div>

  {% if not tareas %}
    <p>No hay tareas todavía.</p>
  {% else %}
    <ul>
      {% for tarea in tareas %}
        <li>
          <span class="{% if tarea[2] %}tachada{% endif %}">{{ tarea[1] }}</span>
          <div class="acciones">
            {% if not tarea[2] %}
              <form method="post" action="/tareas/{{ tarea[0] }}/hecha" style="margin: 0;">
                <button type="submit" class="btn-hecha">Hecha</button>
              </form>
            {% endif %}
            <form method="post" action="/tareas/{{ tarea[0] }}/borrar" style="margin: 0;">
              <button type="submit" class="btn-borrar">Borrar</button>
            </form>
          </div>
        </li>
      {% endfor %}
    </ul>
  {% endif %}
</body>
</html>
from fastapi import FastAPI

app = FastAPI()

#Poner que la app empieze em /api
@app.get("/api")
def api_root():
    return {"mensaje": "Bienvenido a la API"}

# ==========================================
# ENDPOINTS GET (Obtener datos)
# ==========================================

@app.get("/api/home")
def home():
    return {"mensaje": "Bienvenido a la API"}


@app.get("/api/status")
def get_status():
    return {"estado": "activa", "modo": "produccion"}


@app.get("/api/usuarios")
def get_usuarios():
    # Ejemplo de devolución de una lista simple
    return [
        {"id": 1, "nombre": "Alice"},
        {"id": 2, "nombre": "Bob"}
    ]


# ==========================================
# ENDPOINTS POST (Enviar datos)
# ==========================================

@app.post("/api/usuarios")
def crear_usuario(nombre: str):
    return {"mensaje": "Usuario creado", "nombre": nombre}
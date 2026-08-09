from fastapi import FastAPI

app = FastAPI()

# ==========================================
# ENDPOINTS GET (Obtener datos)
# ==========================================

@app.get("/")
def home():
    return {"mensaje": "Bienvenido a la API"}


@app.get("/status")
def get_status():
    return {"estado": "activa", "modo": "produccion"}


@app.get("/usuarios")
def get_usuarios():
    # Ejemplo de devolución de una lista simple
    return [
        {"id": 1, "nombre": "Alice"},
        {"id": 2, "nombre": "Bob"}
    ]


# ==========================================
# ENDPOINTS POST (Enviar datos)
# ==========================================

@app.post("/usuarios")
def crear_usuario(nombre: str):
    return {"mensaje": "Usuario creado", "nombre": nombre}
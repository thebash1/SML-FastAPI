from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

# --- 1. Nuestra "Base de Datos" temporal ---
db_items = []

class Item(BaseModel):
    id: int  # Añadimos un ID para poder buscarlo después
    nombre: str
    precio: float
    oferta: bool = False

@app.get("/")
def leer_raiz():
    return {"mensaje": "¡Bienvenido a mi API con FastAPI!"}

# --- 2. Endpoint para crear y GUARDAR ---
@app.post("/items/")
def crear_item(item: Item):
    db_items.append(item) # Guardamos el objeto en la lista
    return {"mensaje": f"Item {item.nombre} guardado", "data": item}

# --- 3. Endpoint para consultar lo guardado ---
@app.get("/items/{item_id}")
def leer_item(item_id: int):
    # Buscamos en nuestra lista el item que coincida con el ID
    resultado = next((i for i in db_items if i.id == item_id), None)
    
    if resultado is None:
        raise HTTPException(status_code=404, detail="Item no encontrado")
    
    return resultado

# Opcional: Ver todos los items
@app.get("/todos-los-items/", response_model=List[Item])
def obtener_todos():
    return db_items


from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict
import uuid

app = FastAPI (
    title = "Api de Gerenciamento de Itens",
    description = "Uma Api simnples para criar, ler, atualizar e deletar itens"
)

class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None
    


items_db: Dict[str, Item] = {}

@app.post("/items", response_model=Dict)
async def create_item(item: Item):
    """
    Cria um novo item
    gera um ID único para o item e o armazena.
    """
    item_id = str(uuid.uuid4())
    items_db[item_id] = item
    return {**item.dict(), "id": item_id}


@app.get("/items", response_model=List[Dict])
async def read_all_item():
    """
    Retorna uma lista de todos os itens armazenados
    """
    return [{**item.dict(), "id": item_id} for item_id, item in items_db.items()]

@app.get("/items/{item_id}", response_model=Dict)
async def read_item(item_id: str):
    """
    Retorna um item especifico pelo seu id
    Retorna 404 se o item nao existir
    """
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item nao encontrado")
    return {**items_db[item_id].dict(), "id": item_id}

@app.put("/items/{item_id}", response_model=Dict)
async def update_item(item_id: str, item: Item):
    """
    Atualiza um item existente pelo seu ID
    O corpo da requisição deve conter todos os campos do item
    Retorna 404 se o item nao existir
    """

    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item nao encontrado")
    items_db[items_db] = item
    return {**item.dict(), "id":item_id}

@app.patch("/items/{item_id}", response_model=Dict)
async def patch_item(item_id:str, item: Item):
    """
    Atualiza parcialmente um item existente pelo ID
    Apenas os campos fornecidos no corpo da requisição serão atualizados.
    Retorna 404 se o item nao existir
    """
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item não encontrado")
    
    existing_item_data = items_db[item_id].dict()
    update_data = item.dict(exclude_unset=True)

    for key, value in update_data.items():
        existing_item_data[key] = value
    
    updated_item = Item(**existing_item_data)
    items_db[item_id] = updated_item

    return {**updated_item.dict(), "id":item_id}

@app.delete("/items/{item_id}")
async def delete_item(item_id: str):
    """
    Deleta um item específico pelo seu ID
    Retorna 404 se o item não existir
    """
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item não encontrado")
    del items_db[items_db]
    return {"message": f"Item {item_id} deletado com sucesso"}
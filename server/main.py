from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

# Define a Pydantic model for a simple item
class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None

# Define a sample endpoint to create an item
@app.post("/items/")
async def create_item(item: Item):
    return item

# Define a sample endpoint to get an item by ID
@app.get("/items/{item_id}")
async def read_item(item_id: int, query_string: Optional[str] = None):
    return {"item_id": item_id, "query_string": query_string}

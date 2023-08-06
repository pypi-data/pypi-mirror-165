from typing import Union
from fastapi import FastAPI
from pyexql.validate import get_sf


app = FastAPI()


@app.get("/")
def read_root():
    return get_sf()


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

import hashlib
from typing import Optional

from fastapi import FastAPI

app = FastAPI()


def get_hash_modulo(id: str, buckets: int = 2) -> int:
    """
    Generates a pseudorandom group assignment using MD5 and a modulus.
    """
    digest = hashlib.md5(id.encode('ascii')).digest()
    int_value = int.from_bytes(digest, byteorder='big')
    return int_value % buckets


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}


@app.get("/exp_group/{id}")
def get_group(id: str):
    exp_group = get_hash_modulo(id)
    return {"exp_group": exp_group}

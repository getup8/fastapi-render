import hashlib
from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Exp(BaseModel):
    num_groups: int | None = 2
    ids: list[str]


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


@app.post("/exp_group_list/")
async def get_exp_groups(ids: list[str]):
    """Get experiment groups for a list of strings.

    This can be sent a raw JSON list like:
    ["hello", "world"]
    """
    return {
        "results": [
            {
                "id": id,
                "group": get_hash_modulo(id)
            }
            for id in ids
        ]
    }


@app.post("/exp_group_list2/")
async def get_exp_groups2(exp: Exp):
    """Get experiment groups for a list of strings.

    This should be sent JSON like:
    {
        "num_groups": 3,
        "ids": ["hello", "world"]
    }

    or if you just want the default of 2 groups:

    {
        "ids": ["hello", "world"]
    }
    """
    return {
        "results": [
            {
                "id": id,
                "group": get_hash_modulo(id, exp.num_groups)
            }
            for id in exp.ids
        ]
    }

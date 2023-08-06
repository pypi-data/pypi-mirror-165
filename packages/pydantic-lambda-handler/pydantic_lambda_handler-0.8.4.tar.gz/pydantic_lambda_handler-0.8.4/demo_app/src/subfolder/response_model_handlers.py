from typing import Optional

from handler_app import plh
from pydantic import BaseModel


class FunModel(BaseModel):
    item_name: str
    item_value: Optional[int]


class ListFunModel(BaseModel):
    __root__: list[FunModel]


@plh.get("/response_model", response_model=FunModel)
def response_model(secret):
    return {"item_name": secret}


@plh.get("/list_response")
def response_list():
    return [{"item_name": 1}]


@plh.get("/list_response_model", response_model=ListFunModel)
def response_list_model():
    return [{"item_name": "secret"}]

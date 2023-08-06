from typing import Optional

from handler_app import plh
from pydantic import BaseModel


class FunModel(BaseModel):
    item_name: str
    item_value: Optional[int]


@plh.get("/response_model", response_model=FunModel)
def response_model(secret):
    return {"item_name": secret}

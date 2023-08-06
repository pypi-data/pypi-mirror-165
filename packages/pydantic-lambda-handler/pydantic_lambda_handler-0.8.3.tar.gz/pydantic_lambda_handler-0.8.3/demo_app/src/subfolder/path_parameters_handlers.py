from enum import Enum

from handler_app import plh  # type: ignore


@plh.get("/teapot", status_code=418)
def hello_teapot():
    return {"message": "I'm a teapot"}


@plh.get("/pets/{petId}", operation_id="Create Pet")
def pets_handler(petId):
    return {"pet_id": petId}


@plh.get("/items/{item_id}")
def handler_with_type_hint(item_id: int):
    return {"item_id": item_id}


class Animals(str, Enum):
    dog = "dog"


@plh.get("/item_enum/{item_id}")
def handler_with_enum_type_hint(item_id: Animals):
    return {"item_id": item_id}

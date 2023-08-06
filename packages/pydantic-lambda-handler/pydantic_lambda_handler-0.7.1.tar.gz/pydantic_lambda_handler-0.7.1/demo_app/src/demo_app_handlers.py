from typing import Optional

from handler_app import plh
from pydantic import BaseModel


class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None


@plh.post("/hello")
def create_handler(item: Item):
    return item


@plh.get("/hello")
def hello_handler():
    from pydantic_core import SchemaValidator, ValidationError

    v = SchemaValidator(
        {
            "type": "typed-dict",
            "fields": {
                "name": {
                    "schema": {
                        "type": "str",
                    },
                },
                "age": {
                    "schema": {
                        "type": "int",
                        "ge": 18,
                    },
                },
                "is_developer": {
                    "schema": {
                        "type": "bool",
                    },
                    "default": True,
                },
            },
        }
    )

    r1 = v.validate_python({"name": "Samuel", "age": 35})
    assert r1 == {"name": "Samuel", "age": 35, "is_developer": True}

    # pydantic-core can also validate JSON directly
    r2 = v.validate_json('{"name": "Samuel", "age": 35}')
    assert r1 == r2

    try:
        v.validate_python({"name": "Samuel", "age": 11})
    except ValidationError:
        """
        1 validation error for model
        age
          Input should be greater than or equal to 18
          [kind=greater_than_equal, context={ge: 18}, input_value=11, input_type=int]
        """
    return {"message": "Hello World"}


@plh.post("/")
def index_handler():
    return {"message": "Hello Index"}

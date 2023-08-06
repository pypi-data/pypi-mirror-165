# Pydantic Lambda handler

The aim is to create something between FastApi and Chalice.
So same familiar interface as FastAPI, where it makes sense, for aws lambda.

The outputs an open api spec as well as a cdk conf which can be used to generate aws gateway and lambdas.

## Basic usage

handler_app.py
```
from pydantic_lambda_handler.main import PydanticLambdaHandler

app = PydanticLambdaHandler(title="PydanticLambdaHandler")
```
{: .language-python}

Then in your file, (file name must end with `_handler.py` or `_handlers.py`

```
app.get("/")
def your_handler():
    return {"success": True}
```
{: .language-python}

## url parameters



## query parameters



## response model

If response model needs to be a list, do need to adjust the model like so

```
class FunModel(BaseModel):
    item_name: str
    item_value: Optional[int]

class ListFunModel(BaseModel):
    __root__: list[FunModel]
```
{: .language-python}
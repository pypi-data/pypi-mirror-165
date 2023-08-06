import re
from inspect import signature
from typing import Any

from awslambdaric.lambda_context import LambdaContext
from openapi_schema_pydantic.v3.v3_0_3 import (
    Info,
    OpenAPI,
    Operation,
    PathItem,
    Response,
)
from openapi_schema_pydantic.v3.v3_0_3.util import (
    PydanticSchema,
    construct_open_api_with_schema_class,
)
from pydantic import BaseModel, create_model

from pydantic_lambda_handler.main import PydanticLambdaHandler
from pydantic_lambda_handler.middleware import BaseHook


class APIGenerationHook(BaseHook):
    """Gen open api"""

    title: str = "Pydantic Lambda Handler"
    version: str = "0.0.0"
    paths: dict[str, PathItem] = {}
    method = None

    @classmethod
    def method_init(cls, **kwargs):
        app: PydanticLambdaHandler = kwargs["self"]
        status_code = kwargs["status_code"]
        open_api_status_code = str(int(status_code))
        cls.method = kwargs["method"]
        response_model = kwargs["response_model"]

        APIGenerationHook.title = app.title
        APIGenerationHook.version = app.version

        if response_model:
            schema = {"schema": PydanticSchema(schema_class=response_model)}
        else:
            schema = {}

        url = kwargs["url"]
        if url in cls.paths:
            setattr(
                cls.paths[url],
                cls.method,
                Operation(
                    responses={
                        open_api_status_code: Response(
                            description=kwargs["description"],
                            content={"application/json": schema},
                        )
                    }
                ),
            )

        else:
            cls.paths[url] = PathItem(
                **{
                    cls.method: Operation(
                        responses={
                            open_api_status_code: Response(
                                description=kwargs["description"],
                                content={"application/json": schema},
                            )
                        }
                    )
                },
            )

        if kwargs["operation_id"]:
            getattr(cls.paths[url], cls.method).operationId = kwargs["operation_id"]

    @classmethod
    def pre_path(cls, **kwargs) -> None:
        sig = signature(kwargs["func"])

        if sig.parameters:

            url = kwargs["url"]

            path_model_dict = {}
            query_model_dict = {}

            body_model = None

            path_parameters_list = list(re.findall(r"\{(.*?)\}", url))
            path_parameters = set(path_parameters_list)

            if len(path_parameters_list) != len(path_parameters):
                raise ValueError(f"re-declared path variable: {url}")

            for param, param_info in sig.parameters.items():
                if issubclass(param_info.annotation, LambdaContext):
                    continue

                if param in path_parameters:
                    if param_info.annotation == param_info.empty:
                        annotations = str, ...
                    else:
                        annotations = param_info.annotation, ...
                else:
                    default = ... if param_info.default == param_info.empty else param_info.default
                    if param_info.annotation == param_info.empty:
                        annotations = str, default
                    else:
                        annotations = param_info.annotation, default

                if param in path_parameters:
                    if param_info.default != param_info.empty:
                        raise ValueError("Should not set default for path parameters")
                    path_model_dict[param] = annotations
                else:
                    model, body_default = annotations
                    if issubclass(model, BaseModel):
                        if body_model:
                            raise ValueError("Can only use one Pydantic model for body only")
                        body_model: BaseModel = model  # type: ignore
                        body_model._alias = param  # type: ignore
                    else:
                        query_model_dict[param] = annotations

            if path_parameters != set(path_model_dict.keys()):
                raise ValueError("Missing path parameters")

            APIPathModel = create_model("APIPathModel", **path_model_dict, **query_model_dict)  # type: ignore

            path_schema_initial = APIPathModel.schema()
            properties = []
            for name, property_info in path_schema_initial.get("properties", {}).items():
                #  {"name": "petId", "in": "path", "required": True, "schema": {"type": "string"}}
                in_ = "path" if name in path_parameters else "query"
                p = {"name": name, "in": in_, "schema": {"type": property_info.get("type", "string")}}
                if name in path_schema_initial.get("required", ()):
                    p["required"] = True

                properties.append(p)

            getattr(cls.paths[url], cls.method).parameters = properties  # type: ignore
            if body_model:
                getattr(cls.paths[url], cls.method).requestBody = {  # type: ignore
                    "content": {"application/json": {"schema": PydanticSchema(schema_class=body_model)}}
                }

    @classmethod
    def pre_func(cls, event, context) -> tuple[dict, LambdaContext]:
        return event, context

    @classmethod
    def post_func(cls, body) -> Any:
        return body

    @classmethod
    def generate(cls):
        open_api = OpenAPI(
            info=Info(title=cls.title, version=cls.version),
            paths=cls.paths,
        )
        open_api = construct_open_api_with_schema_class(open_api)
        return open_api.json(by_alias=True, exclude_none=True, indent=2)

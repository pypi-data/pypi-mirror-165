"""
The main class which you import and use a decorator.
"""
import functools
import json
import re
from http import HTTPStatus
from inspect import signature
from typing import Iterable, Optional, Union

from awslambdaric.lambda_context import LambdaContext
from orjson import loads
from pydantic import BaseModel, ValidationError, create_model

from pydantic_lambda_handler.middleware import BaseHook
from pydantic_lambda_handler.models import BaseOutput


class PydanticLambdaHandler:
    """
    The decorator handle.
    """

    _hooks: list[type[BaseHook]] = []

    def __init__(
        self, *, title="PydanticLambdaHandler", version="0.0.0", hooks: Optional[Iterable[type[BaseHook]]] = None
    ):
        self.title = title
        self.version = version
        if hooks:
            PydanticLambdaHandler._hooks.extend(hooks)

    @classmethod
    def add_hook(cls, hook: type[BaseHook]):
        cls._hooks.append(hook)

    def get(
        self,
        url,
        *,
        status_code: Union[HTTPStatus, int] = HTTPStatus.OK,
        operation_id: str = None,
        description: str = "Successful Response",
        function_name=None,
        response_model=None,
    ):
        """Expect request with a GET method.

        :param url:
        :param status_code:
        :return:
        """
        method = "get"
        return self.run_method(
            method,
            url,
            status_code,
            operation_id,
            description,
            function_name,
            response_model,
        )

    def post(
        self,
        url,
        *,
        status_code: Union[HTTPStatus, int] = HTTPStatus.CREATED,
        operation_id: str = None,
        description: str = "Successful Response",
        function_name=None,
        response_model=None,
    ):
        """Expect request with a POST method.

        :param url:
        :param status_code:
        :return:
        """
        method = "post"
        return self.run_method(
            method,
            url,
            status_code,
            operation_id,
            description,
            function_name,
            response_model,
        )

    def run_method(
        self,
        method,
        url,
        status_code,
        operation_id,
        description,
        function_name,
        response_model,
    ):
        for hook in self._hooks:
            hook.method_init(**locals())

        def create_response(func):
            for hook in self._hooks:
                hook.pre_path(**locals())

            sig = signature(func)

            if sig.parameters:
                EventModel = self.generate_event_model(url, sig)

            @functools.wraps(func)
            def wrapper_decorator(event, context: LambdaContext):
                for hook in self._hooks:
                    event, context = hook.pre_func(event, context)

                sig = signature(func)

                if sig.parameters:
                    path_parameters = event.get("pathParameters", {}) or {}
                    query_parameters = event.get("queryStringParameters", {}) or {}

                    if event["body"] is not None:
                        body = loads(event["body"])
                    else:
                        body = None

                    try:
                        event_model = EventModel(path=path_parameters, query=query_parameters, body=body)
                    except ValidationError as e:
                        response = BaseOutput(
                            body=json.dumps({"detail": json.loads(e.json())}),
                            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
                        )
                        return loads(response.json())

                    # Do something before
                    func_kwargs = {**event_model.path.dict(), **event_model.query.dict()}
                    if hasattr(event_model, "body"):
                        func_kwargs.update(**{event_model.body._alias: event_model.body})

                    if context_name := next(
                        (i.name for i in iter(sig.parameters.values()) if issubclass(i.annotation, LambdaContext)), None
                    ):
                        func_kwargs[context_name] = context
                    body = func(**func_kwargs)
                else:
                    body = func()

                for hook in reversed(self._hooks):
                    body = hook.post_func(body)

                if hasattr(body, "json"):
                    response = BaseOutput(body=body.json(), status_code=status_code)
                else:
                    response = BaseOutput(body=json.dumps(body), status_code=status_code)

                return loads(response.json())

            return wrapper_decorator

        for hook in self._hooks:
            hook.post_create_response(**locals())
        return create_response

    @staticmethod
    def generate_event_model(url, sig):
        path_model_dict = {}
        query_model_dict = {}

        body_default = None
        body_model = None

        path_parameters_list = list(re.findall(r"\{(.*?)\}", url))
        path_parameters = set(path_parameters_list)
        additional_kwargs = {}
        if len(path_parameters_list) != len(path_parameters):
            raise ValueError(f"re-declared path variable: {url}")
        for param, param_info in sig.parameters.items():
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
                    body_model = model
                    body_model._alias = param
                elif issubclass(model, LambdaContext):
                    additional_kwargs[param] = annotations
                else:
                    query_model_dict[param] = annotations

        if path_parameters != set(path_model_dict.keys()):
            raise ValueError("Missing path parameters")

        PathModel = create_model("PathModel", **path_model_dict)
        QueryModel = create_model("QueryModel", **query_model_dict)
        event_models = {"path": (PathModel, {}), "query": (QueryModel, {})}
        if body_model:
            event_models["body"] = (body_model, body_default)

        return create_model("EventModel", **event_models)

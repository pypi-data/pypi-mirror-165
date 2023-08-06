from collections import defaultdict
from typing import Any

from awslambdaric.lambda_context import LambdaContext

from pydantic_lambda_handler.middleware import BaseHook


class MockRequests(BaseHook):
    testing_stuff: dict = defaultdict(dict)
    _testing_url = None
    _method = None

    @classmethod
    def method_init(cls, **kwargs):
        url = kwargs["url"]
        cls._method = kwargs["method"]

        cls._testing_url = url.replace("{", "(?P<").replace("}", r">\w+)")
        if cls._testing_url not in cls.testing_stuff["paths"]:
            cls.testing_stuff["paths"][cls._testing_url] = {cls._method: {}}
        else:
            cls.testing_stuff["paths"][cls._testing_url][cls._method] = {}

    @classmethod
    def pre_path(cls, **kwargs) -> None:
        func = kwargs["func"]
        cls.testing_stuff["paths"][cls._testing_url][cls._method]["handler"]["function"] = func

    @classmethod
    def pre_func(cls, event, context) -> tuple[dict, LambdaContext]:
        return event, context

    @classmethod
    def post_func(cls, body) -> Any:
        return body

    @classmethod
    def post_create_response(cls, **kwargs):
        create_response = kwargs["create_response"]

        cls.testing_stuff["paths"][cls._testing_url][cls._method]["handler"] = {"decorated_function": create_response}
        return {}


def add_resource(child_dict: dict, url):
    part, found, remaining = url.partition("/")
    if part:
        if part in child_dict.get("resources", {}):
            return add_resource(child_dict["resources"][part], remaining)

        last_resource: dict[str, dict] = {}
        if "resources" not in child_dict:
            child_dict["resources"] = {part: last_resource}
        else:
            child_dict["resources"].update({part: last_resource})

        return add_resource(child_dict["resources"][part], remaining)
    return child_dict


def to_camel_case(text):
    s = text.replace("-", " ").replace("_", " ")
    s = s.split()
    if len(text) == 0:
        return text.capitalize()
    return "".join(i.capitalize() for i in s)

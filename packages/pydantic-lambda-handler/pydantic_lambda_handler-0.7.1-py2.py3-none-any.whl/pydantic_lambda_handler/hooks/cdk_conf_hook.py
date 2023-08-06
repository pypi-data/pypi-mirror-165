import inspect
from collections import defaultdict
from pathlib import Path
from typing import Any

from awslambdaric.lambda_context import LambdaContext

from pydantic_lambda_handler.middleware import BaseHook


class CDKConf(BaseHook):
    """Gen cdk conf"""

    _dir_path: Path
    _method = None
    _hold_dict: dict = defaultdict(dict)

    @classmethod
    def method_init(cls, **kwargs):
        cls._method = kwargs["method"].upper()
        cls._hold_dict[kwargs["url"]].update(
            {
                cls._method: {
                    "function_name": kwargs["function_name"],
                    "status_code": str(int(kwargs["status_code"])),
                }
            }
        )

    @classmethod
    def pre_path(cls, **kwargs) -> None:
        func = kwargs["func"]
        cls._hold_dict[kwargs["url"]][cls._method]["index"] = str(
            Path(inspect.getfile(func)).relative_to(cls._dir_path)
        )
        cls._hold_dict[kwargs["url"]][cls._method]["handler"] = func.__name__
        cls._hold_dict[kwargs["url"]][cls._method]["reference"] = f"{func.__module__}.{func.__qualname__}"
        cls._hold_dict[kwargs["url"]][cls._method]["function_name"] = cls._hold_dict[kwargs["url"]][cls._method][
            "function_name"
        ] or to_camel_case(func.__name__)

    @classmethod
    def pre_func(cls, event, context) -> tuple[dict, LambdaContext]:
        return event, context

    @classmethod
    def post_func(cls, body) -> Any:
        return body

    @classmethod
    def generate(cls):

        methods = ("GET", "POST")

        resource = []
        for url, conf in sorted(cls._hold_dict.items()):
            add_resource_v2(resource, url, conf)

        def sort_recursive(resource_list: list[dict]):
            resource_list.sort(key=lambda x: x.get("name", ""))
            seen = set()
            for i in resource_list:
                if "methods" in i:
                    i["methods"] = sorted(i["methods"], key=lambda x: methods.index(x["method"]))

                if i["name"] in seen:
                    raise ValueError(f'{i["name"]=}')

                seen.add(i["name"])

                if "resources" in i:
                    sort_recursive(i["resources"])

        sort_recursive(resource)
        return resource


def add_resource_v2(child_list: list[dict], url: str, conf):
    name, found, remaining = url.partition("/")

    if not name and not remaining:
        # at "/"
        methods: list[dict] = []
        child_list.append({"methods": methods, "name": name})
        for method, method_conf in conf.items():
            methods.append(add_method_v2(method, method_conf))
        return
    elif not name and remaining:
        # "", "/" query
        if not child_list:
            child_resource = {}
            resources: list[dict] = []
            child_resource["resources"] = resources
            child_list.append(child_resource)
            add_resource_v2(resources, remaining, conf)
        else:
            child_list_ = child_list[0]
            if "resources" in child_list_:
                resources = child_list_["resources"]
            else:
                resources = []
                child_list_["resources"] = resources

            add_resource_v2(resources, remaining, conf)

    elif name and remaining:
        # need to keep traversing
        child_resource = next((i for i in child_list if i.get("name") == name), None)  # type: ignore
        if not child_resource:
            resources = []
            child_resource = {"name": name, "resources": resources}  # type: ignore
            child_list.append(child_resource)
            add_resource_v2(resources, remaining, conf)
        else:
            print()
    else:
        # add methods
        child_resource = next((i for i in child_list if i.get("name") == name), None)  # type: ignore
        if not child_resource:
            child_resource = {"name": name}  # type: ignore
            child_list.append(child_resource)
        else:
            print()

        if "methods" in child_resource:
            methods = child_resource["methods"]
        else:
            methods = []
            child_resource["methods"] = methods

        for method, method_conf in conf.items():
            methods.append(add_method_v2(method, method_conf))

    return child_list


def to_camel_case(text):
    s = text.replace("-", " ").replace("_", " ")
    s = s.split()
    if len(text) == 0:
        return text.capitalize()
    return "".join(i.capitalize() for i in s)


def add_method_v2(method, conf):
    return {
        "method": method,
        "index": conf["index"],
        "handler": conf["handler"],
        "reference": conf["reference"],
        "status_code": conf["status_code"],
        "function_name": conf["function_name"],
    }

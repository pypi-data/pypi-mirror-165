import json
import os
import sys
from ast import Import, ImportFrom, parse, walk
from copy import deepcopy
from importlib.util import module_from_spec, spec_from_file_location
from inspect import getmembers
from pathlib import Path
from sys import modules
from typing import Optional

from pydantic_lambda_handler.hooks.cdk_conf_hook import CDKConf
from pydantic_lambda_handler.hooks.mock_requests import MockRequests
from pydantic_lambda_handler.hooks.open_api_gen_hook import APIGenerationHook
from pydantic_lambda_handler.main import PydanticLambdaHandler


def get_top_imported_names(file: str) -> set[str]:
    """Collect names imported in given file.

    We only collect top-level names, i.e. `from foo.bar import baz`
    will only add `foo` to the list.
    """
    if not file.endswith(".pyi"):
        return set()
    with open(os.path.join(file), "rb") as f:
        content = f.read()
    parsed = parse(content)
    top_imported = set()
    for node in walk(parsed):
        if isinstance(node, Import):
            for name in node.names:
                top_imported.add(name.name.split(".")[0])
        elif isinstance(node, ImportFrom):
            if node.level > 0:
                # Relative imports always refer to the current package.
                continue
            assert node.module
            top_imported.add(node.module.split(".")[0])
    return top_imported


class add_path:
    def __init__(self, path):
        self.path = str(path)
        self.added = False

    def __enter__(self):
        if self.path not in sys.path:
            sys.path.insert(0, self.path)
            self.added = True

    def __exit__(self, exc_type, exc_value, traceback):
        if self.added:
            try:
                sys.path.remove(self.path)
            except ValueError:
                pass


def gen_open_api_inspect(dir_path: Path):
    with add_path(dir_path):
        files = list(dir_path.rglob("*_handlers.py"))
        app_fp = dir_path.joinpath("app.py")
        if app_fp.exists():
            files.insert(0, app_fp)
        else:
            files.insert(0, dir_path.joinpath("handler_app.py"))

        print(list(files))

        # This is ugly, once it works refactor out
        PydanticLambdaHandler.add_hook(APIGenerationHook)
        CDKConf._dir_path = dir_path
        PydanticLambdaHandler.add_hook(CDKConf)
        PydanticLambdaHandler.add_hook(MockRequests)

        app: Optional[PydanticLambdaHandler] = None

        for file in files:
            module_name = ".".join(str(file.relative_to(dir_path)).removesuffix(".py").split("/"))
            spec = spec_from_file_location(module_name, file)
            if not spec or not spec.loader:
                continue
            module = module_from_spec(spec)
            modules[module_name] = module
            spec.loader.exec_module(module)
            results = getmembers(module)

            for i in range(len(results)):
                if isinstance(results[i][1], PydanticLambdaHandler):
                    app = deepcopy(results[i][1])

        if app:
            return (
                next(h for h in app._hooks if issubclass(h, APIGenerationHook)).generate(),  # type: ignore
                next(h for h in app._hooks if issubclass(h, CDKConf)).generate(),  # type: ignore
                next(h for h in app._hooks if issubclass(h, MockRequests)).testing_stuff,  # type: ignore
            )
        raise ValueError("App not found")


def main():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("app_dir")
    parser.add_argument("output_file_path")
    args = parser.parse_args()

    app_dir = args.app_dir
    output_file_path = args.output_file_path

    app_dir_path = Path(app_dir)
    app_dir_path.exists()

    schema, *_ = gen_open_api_inspect(app_dir_path)

    output_file_path = Path(output_file_path)
    output_file_path.parent.exists()

    schema = json.loads(schema)

    with output_file_path.open("w") as f:
        json.dump(schema, f, indent=4)


def cdk_conf():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("app_dir")
    parser.add_argument("output_file_path")
    args = parser.parse_args()

    app_dir = args.app_dir
    output_file_path = args.output_file_path

    app_dir_path = Path(app_dir)
    app_dir_path.exists()

    _, cdk_conf, _ = gen_open_api_inspect(app_dir_path)

    output_file_path = Path(output_file_path)
    output_file_path.parent.exists()

    with output_file_path.open("w") as f:
        json.dump(cdk_conf, f, indent=4)

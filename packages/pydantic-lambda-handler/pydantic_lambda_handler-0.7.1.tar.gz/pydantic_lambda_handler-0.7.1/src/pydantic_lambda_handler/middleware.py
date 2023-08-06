from typing import Any

from awslambdaric.lambda_context import LambdaContext


class BaseHook:
    @staticmethod
    def method_init(**kwargs) -> None:
        return

    @staticmethod
    def pre_path(**kwargs) -> None:
        return

    @staticmethod
    def pre_func(event, context) -> tuple[dict, LambdaContext]:
        return event, context

    @staticmethod
    def post_func(body) -> Any:
        return body

    @staticmethod
    def post_create_response(**kwargs) -> None:
        return

from awslambdaric.lambda_context import LambdaContext
from handler_app import plh

fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]


@plh.get("/context")
def with_context(lambda_context: LambdaContext):
    return {"context": lambda_context.get_remaining_time_in_millis()}

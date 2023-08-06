from handler_app import plh

fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]


@plh.get("/query")
def query_skip(skip: int = 0, limit: int = 10):
    return fake_items_db[skip : skip + limit]


@plh.get("/query_required")
def query_required(secret):
    return {"item_name": secret}

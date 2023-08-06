def test_generate_open_api_version(schema):
    assert schema["openapi"] == "3.0.3"


def test_generate_open_api_info(schema):
    assert schema["info"] == {"title": "PydanticLambdaHandler", "version": "0.0.0"}


def test_generate_open_api_info_path_get(schema):
    item_path = schema["paths"]["/hello"]["get"]["responses"]["200"]["content"]
    assert item_path == {"application/json": {}}


def test_generate_open_api_info_path_post(schema):
    item_path = schema["paths"]["/hello"]["post"]["responses"]["201"]["content"]
    assert item_path == {"application/json": {}}


def test_generate_open_api_list_response_model(schema):
    item_path = schema["paths"]["/list_response_model"]["get"]["responses"]["200"]["content"]
    assert item_path == {"application/json": {"schema": {"$ref": "#/components/schemas/ListFunModel"}}}
    assert schema["components"]["schemas"]["ListFunModel"] == {
        "items": {"$ref": "#/components/schemas/FunModel"},
        "title": "ListFunModel",
        "type": "array",
    }


def test_query_body(schema):
    request_schema = schema["paths"]["/hello"]["post"]["requestBody"]["content"]["application/json"]["schema"]
    assert request_schema == {"$ref": "#/components/schemas/Item"}
    assert schema["components"]["schemas"]["Item"] == {
        "properties": {
            "description": {"title": "Description", "type": "string"},
            "name": {"title": "Name", "type": "string"},
            "price": {"title": "Price", "type": "number"},
            "tax": {"title": "Tax", "type": "number"},
        },
        "required": ["name", "price"],
        "title": "Item",
        "type": "object",
    }


def test_generate_open_api_status_code_int(schema):
    """Can accept an in or an Enum status code"""
    assert "418" in schema["paths"]["/teapot"]["get"]["responses"]


def test_generate_open_api_path(schema):
    assert "/pets/{petId}" in schema["paths"]
    assert schema["paths"]["/pets/{petId}"]["get"].get("parameters") == [
        {"name": "petId", "in": "path", "required": True, "schema": {"type": "string"}}
    ]


def test_generate_open_operation_id(schema):
    assert schema["paths"]["/pets/{petId}"]["get"].get("operationId") == "Create Pet"


def test_query_options(schema):
    assert "/query" in schema["paths"]
    assert schema["paths"]["/query"]["get"].get("parameters") == [
        {"in": "query", "name": "skip", "schema": {"type": "integer"}},
        {"in": "query", "name": "limit", "schema": {"type": "integer"}},
    ]


def test_response_body(schema):
    assert "/response_model" in schema["paths"]
    response_schema = schema["paths"]["/response_model"]["get"]["responses"]["200"]["content"]["application/json"][
        "schema"
    ]
    assert response_schema == {"$ref": "#/components/schemas/FunModel"}
    assert schema["components"]["schemas"]["FunModel"] == {
        "title": "FunModel",
        "required": ["item_name"],
        "type": "object",
        "properties": {
            "item_name": {"title": "Item Name", "type": "string"},
            "item_value": {"title": "Item Value", "type": "integer"},
        },
    }

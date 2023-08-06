from demo_app_handlers import create_handler  # type: ignore


def test_get_response(requests_client, base_url):
    """
    test that the message is returned to the body
    """
    response = requests_client.get(f"{base_url}/hello")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}


def test_post_response(requests_client, base_url):
    """
    test that the message is returned to the body
    """
    body = {"name": "Foo", "description": "An optional description", "price": 45.2, "tax": 3.5}
    response = requests_client.post(f"{base_url}/hello", json=body)
    assert response.status_code == 201, response.json()
    assert response.json() == body


def test_post_invalid_body(requests_client, base_url):
    """
    test that the message is returned to the body
    """
    body = {
        "description": "An optional description",
        "price": 45.2,
    }
    response = requests_client.post(f"{base_url}/hello", json=body)
    assert response.status_code == 422
    assert response.json() == {
        "detail": [{"loc": ["body", "name"], "msg": "field required", "type": "value_error.missing"}]
    }


def test_inv(mock_lambda_context):
    event = {
        "resource": "/hello",
        "path": "/hello",
        "httpMethod": "POST",
        "queryStringParameters": None,
        "body": '{"name": "Foo", "description": "An optional description", "price": 45.2, "tax": 3.5}',
        "isBase64Encoded": False,
    }

    response = create_handler(event, mock_lambda_context)

    assert response["statusCode"] == 201, response.get("body")

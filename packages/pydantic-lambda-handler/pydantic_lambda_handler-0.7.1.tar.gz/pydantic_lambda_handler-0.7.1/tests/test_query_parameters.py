def test_no_query(requests_client, base_url):
    response = requests_client.get(f"{base_url}/query")
    assert response.status_code == 200, response.json()
    assert response.json() == [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]


def test_query(requests_client, base_url):
    response = requests_client.get(f"{base_url}/query", params={"skip": 1})
    assert response.status_code == 200, response.json()
    assert response.json() == [{"item_name": "Bar"}, {"item_name": "Baz"}]


def test_missing_query(requests_client, base_url):
    response = requests_client.get(f"{base_url}/query_required")
    assert response.status_code == 422, response.json()
    assert response.json() == {
        "detail": [{"loc": ["query", "secret"], "msg": "field required", "type": "value_error.missing"}]
    }

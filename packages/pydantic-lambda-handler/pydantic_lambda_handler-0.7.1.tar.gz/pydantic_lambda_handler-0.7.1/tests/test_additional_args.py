def test_context(requests_client, base_url):
    response = requests_client.get(f"{base_url}/context")
    assert response.status_code == 200, response.json()
    assert isinstance(response.json()["context"], int)

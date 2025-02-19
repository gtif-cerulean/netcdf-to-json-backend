def test_landing_page_loads(client):
    response = client.get("/")
    assert response.json() == {}

def test_example(client):
    response = client.get("/")
    assert response.status_code == 200

def test_get_doctor(client):
    client.get("/")

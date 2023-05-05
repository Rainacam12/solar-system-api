def test_read_all_planets_returns_empty_list(client):
    # act
    response = client.get("/planets")
    response_body = response.get_json()

    # assert
    assert response.status_code == 200
    assert response_body == []

def test_get_one_planet(client, make_two_planets):
    # Act
    response = client.get("/planets/2")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == {
        "id": 2,
        "name": "Saturn",
        "description": "Gaseous, beige",
        "size": 17
    }

def test_create_planet_route(client):
     # Act
    response = client.post("/planets", json={
        "name": "Mercury",
        "description": "Small, close to the sun",
        "size": 6
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 201
    assert response_body == "Planet Mercury successfully created"

    
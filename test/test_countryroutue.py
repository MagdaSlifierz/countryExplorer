import json


# defind test case
def test_create_country(client, token_header):
    country_data = {
        "country_name": "USA",
        "capital": "Washington",
        "official_lang": "Engilish",
        "description": "The United States of America is the world's third largest country in size and nearly the third largest in terms of population.",
        "user_creator_id": 2,
    }

    response = client.post(
        "/country", json=country_data, headers=token_header
    )  # json.dumps(data)) this change our data to json reprensetation
    assert response.status_code == 200
    assert response.json()["country_name"] == "USA"
    assert response.json()["capital"] == "Washington"
    assert response.json()["official_lang"] == "Engilish"
    assert (
        response.json()["description"]
        == "The United States of America is the world's third largest country in size and nearly the third largest in terms of population."
    )
    assert response.json()["user_creator_id"] == 2


def test_get_country_by_id(client):
    response = client.get("/country/2")
    assert response.status_code == 200
    assert response.json()["country_name"] == "USA"
    assert response.json()["capital"] == "Washington"
    assert response.json()["official_lang"] == "Engilish"
    assert (
        response.json()["description"]
        == "The United States of America is the world's third largest country in size and nearly the third largest in terms of population."
    )

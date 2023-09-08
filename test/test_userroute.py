
#defind test case
def test_create_user(client):
    data = {
        "first_name" : "Anna",
        "last_name" : "Nowak", 
        "email" : "anna.n@gmail.com", 
        "password" : "Nowak123"
        }
    response = client.post("/users", json=data) #json.dumps(data)) this change our data to json reprensetation
    assert response.status_code == 200
    assert response.json()["first_name"] == "Anna"
    assert response.json()["last_name"] == "Nowak"
    assert response.json()["email"] == "anna.n@gmail.com"
    assert response.json()["is_active"] is True
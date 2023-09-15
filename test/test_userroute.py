
#defind test case
def test_create_user(client):
    data = {
        "first_name" : "Angelina",
        "last_name" : "Joli", 
        "email" : "a.j@gmail.com", 
        "password" : "aj123"
        }
    response = client.post("/users", json=data) #json.dumps(data)) this change our data to json reprensetation
    assert response.status_code == 200
    assert response.json()["first_name"] == "Angelina"
    assert response.json()["last_name"] == "Joli"
    assert response.json()["email"] == "a.j@gmail.com"
    assert response.json()["is_active"] is True
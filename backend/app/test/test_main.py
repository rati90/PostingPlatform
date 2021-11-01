from bson import ObjectId, json_util
import json
from fastapi.testclient import TestClient

from ...main import app

client = TestClient(app)

post = {
    "_id": ObjectId("123456781234567812345678"),
    "created_by": "rati@gmail.com",
    "name": "Some books",
    "desc": "more Books",
    "date_created": "10.10.2021",
    "comments": []

}

user = {
    "id": "44556644211",
    "email": "rati@gmail.com",
    "password": "string",
    "first_name": "Rati",
    "last_name": "Bakhtadze"
}


def parse_json(post):
    return json.loads(json_util.dumps(post))


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}


def test_get_post():
    response = client.get("/api/get/post/123456781234567812345678", json=post)
    assert response.status_code == 200





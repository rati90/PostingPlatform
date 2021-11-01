import pytest
from bson import ObjectId, json_util
import json
from fastapi.testclient import TestClient


from main import app

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


@pytest.mark.asyncio
async def test_read_main(client):
    response = await client.get("/")
    
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}

@pytest.mark.asyncio
async def test_get_post(client):
    response = await client.get("/api/get/post/123456781234567812345678")
    assert response.status_code == 200





from app import app
from fastapi.testclient import TestClient
from fastapi import status


client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == status.HTTP_200_OK
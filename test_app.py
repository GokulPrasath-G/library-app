import pytest
import json
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home_route(client):
    response = client.get('/')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert "Library Book Management System" in data["message"]

def test_health_route(client):
    response = client.get('/health')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["status"] == "healthy"

def test_get_books(client):
    response = client.get('/books')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert "books" in data
    assert len(data["books"]) >= 2

def test_add_book_success(client):
    new_book = {"title": "Continuous Delivery", "author": "Jez Humble"}
    response = client.post('/books', json=new_book)
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data["message"] == "Book added successfully"
    assert data["book"]["title"] == "Continuous Delivery"

def test_add_book_missing_data(client):
    incomplete_book = {"title": "Incomplete Book"}
    response = client.post('/books', json=incomplete_book)
    assert response.status_code == 400

def test_issue_book_success(client):
    # Issue existing book with ID 1
    response = client.post('/books/issue', json={"id": 1})
    assert response.status_code == 200
    data = json.loads(response.data)
    assert "successfully issued" in data["message"]
    assert data["book"]["available"] is False

def test_issue_book_already_issued(client):
    # Book 1 was issued in the previous test execution thread
    response = client.post('/books/issue', json={"id": 1})
    assert response.status_code == 400
    data = json.loads(response.data)
    assert "already issued" in data["error"]

def test_issue_book_not_found(client):
    response = client.post('/books/issue', json={"id": 999})
    assert response.status_code == 404

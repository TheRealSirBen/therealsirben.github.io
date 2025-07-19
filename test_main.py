from fastapi.testclient import TestClient
from main import app, load_portfolio_data

# Create a test client
client = TestClient(app)


def test_read_main():
    """
    Test the main page route
    """
    response = client.get("/")
    assert response.status_code == 200
    assert "Benedict Dlamini" in response.text


def test_portfolio_data_loading():
    """
    Test portfolio data loading
    """
    portfolio_data = load_portfolio_data()

    assert 'name' in portfolio_data
    assert 'projects' in portfolio_data
    assert 'skills' in portfolio_data
    assert portfolio_data['name'] == 'Benedict Dlamini'


def test_contact_submission():
    """
    Test contact form submission
    """
    contact_data = {
        "name": "Test User",
        "email": "test@example.com",
        "message": "Test message"
    }

    response = client.post("/contact", data=contact_data)
    assert response.status_code == 200
    assert response.json()['status'] == 'success'


def test_portfolio_api_endpoint():
    """
    Test the portfolio API endpoint
    """
    response = client.get("/api/portfolio")
    assert response.status_code == 200

    data = response.json()
    assert 'name' in data
    assert 'projects' in data
    assert 'skills' in data


def test_404_handler():
    """
    Test custom 404 error handler
    """
    response = client.get("/nonexistent-route")
    assert response.status_code == 404
    assert "Page not found" in response.text

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


def test_contact_form_submission():
    """
    Test contact form submission
    """
    contact_data = {
        "name": "Test User",
        "email": "test@example.com",
        "message": "Test contact form submission"
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


def test_video_publications_data():
    """
    Test video publications data
    """
    portfolio_data = load_portfolio_data()

    assert 'videoPublications' in portfolio_data
    video_pubs = portfolio_data['videoPublications']

    assert 'title' in video_pubs
    assert 'description' in video_pubs
    assert 'date' in video_pubs
    assert 'platform' in video_pubs


def test_static_files():
    """
    Test static file routes
    """
    # Test professional image
    response = client.get("/static/images/benedict-profile.jpg")
    assert response.status_code == 200

    # Test video
    response = client.get("/static/videos/personal-intro.mp4")
    assert response.status_code == 200


def test_social_links():
    """
    Test social links in portfolio data
    """
    portfolio_data = load_portfolio_data()

    assert 'social' in portfolio_data
    social_links = portfolio_data['social']

    assert len(social_links) > 0

    for link in social_links:
        assert 'platform' in link
        assert 'url' in link
        assert 'icon' in link

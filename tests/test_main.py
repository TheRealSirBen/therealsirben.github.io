import os
import pytest
from fastapi.testclient import TestClient
import yaml
import sys

# Add project root to a Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# Import the main application and data loading function
from main import app, load_portfolio_data

# Create a test client
client = TestClient(app)

# Global variable to track created files
CREATED_FILES = []


def create_placeholder_files():
    """
    Create placeholder files for testing static assets
    """
    global CREATED_FILES
    CREATED_FILES.clear()  # Clear previous files

    # Ensure directories exist
    os.makedirs('static/images', exist_ok=True)
    os.makedirs('static/videos', exist_ok=True)
    os.makedirs('static/css', exist_ok=True)
    os.makedirs('static/js', exist_ok=True)
    os.makedirs('static/documents', exist_ok=True)

    # Create placeholder files if they don't exist
    placeholder_files = [
        'static/images/benedict-dlamini.png',
        'static/videos/invideo-ai-personal-intro.mp4',
        'static/css/styles.css',
        'static/js/app.js'
    ]

    for file_path in placeholder_files:
        if not os.path.exists(file_path):
            # Create an empty file
            open(file_path, 'a').close()
            CREATED_FILES.append(file_path)

    return CREATED_FILES


def teardown_module(module):
    """
    Cleanup placeholder files after tests
    """
    global CREATED_FILES
    for file_path in CREATED_FILES:
        if os.path.exists(file_path):
            os.remove(file_path)
    CREATED_FILES.clear()


def test_static_files():
    """
    Test availability of key static files
    """
    # Create placeholder files before testing
    create_placeholder_files()

    # Test image
    response = client.get("/static/images/benedict-dlamini.png")
    assert response.status_code == 200

    # Test video
    response = client.get("/static/videos/invideo-ai-personal-intro.mp4")
    assert response.status_code == 200

    # Test CSS
    response = client.get("/static/css/styles.css")
    assert response.status_code == 200

    # Test JavaScript
    response = client.get("/static/js/app.js")
    assert response.status_code == 200


# Utility function to load test data
def load_test_data():
    """
    Load portfolio data for testing
    """
    return load_portfolio_data()


def test_main_page():
    """
    Test the main page route
    """
    response = client.get("/")
    assert response.status_code == 200

    # Check for key content
    content = response.text
    assert "Benedict Dlamini" in content
    assert "Data Strategy Consultant" in content


def test_portfolio_data_structure():
    """
    Validate the structure of portfolio data
    """
    data = load_test_data()

    # Check for required top-level keys
    required_keys = [
        'name',
        'tagline',
        'professionalImage',
        'projects',
        'skills',
        'social',
        'videoPublications'
    ]

    for key in required_keys:
        assert key in data, f"Missing required key: {key}"


def test_projects_data():
    """
    Validate projects data structure
    """
    data = load_test_data()
    projects = data.get('projects', [])

    assert len(projects) > 0, "No projects found"

    for project in projects:
        # Check required project keys
        required_project_keys = [
            'title',
            'description',
            'technologies',
            'situation',
            'problem',
            'action',
            'results'
        ]

        for key in required_project_keys:
            assert key in project, f"Missing key in project: {key}"

        # Validate specific types
        assert isinstance(project['technologies'], list)
        assert isinstance(project['action'], list)
        assert isinstance(project['results'], list)


def test_skills_data():
    """
    Validate skills data structure
    """
    data = load_test_data()
    skills = data.get('skills', {})

    assert len(skills) > 0, "No skills categories found"

    # Ensure skills are categorized
    expected_categories = [
        'Data Engineering',
        'Data Analytics',
        'Project Management'
    ]

    for category in expected_categories:
        assert category in skills, f"Missing skill category: {category}"

    # Validate skills within categories
    for category, skill_list in skills.items():
        assert isinstance(skill_list, list)
        assert len(skill_list) > 0, f"No skills in {category}"


def test_social_links():
    """
    Validate social links
    """
    data = load_test_data()
    social_links = data.get('social', [])

    assert len(social_links) > 0, "No social links found"

    for link in social_links:
        # Check required social link keys
        required_link_keys = ['platform', 'url', 'icon']
        for key in required_link_keys:
            assert key in link, f"Missing key in social link: {key}"

        # Validate URL format (basic check)
        assert link['url'].startswith(('http://', 'https://', 'mailto:'))


def test_video_publications():
    """
    Validate video publications data
    """
    data = load_test_data()
    video_pubs = data.get('videoPublications', {})

    # Check required video publication keys
    required_video_keys = [
        'title',
        'description',
        'date',
        'platform'
    ]

    for key in required_video_keys:
        assert key in video_pubs, f"Missing key in video publications: {key}"

    # Optional link validation
    if 'link' in video_pubs:
        assert video_pubs['link'].startswith(('http://', 'https://'))


def test_yaml_file_integrity():
    """
    Validate YAML file can be parsed correctly
    """
    try:
        yaml_path = os.path.join('data', 'portfolio.yaml')
        with open(yaml_path, 'r') as file:
            data = yaml.safe_load(file)

        assert data is not None, "YAML file is empty or invalid"
    except Exception as e:
        pytest.fail(f"Error parsing YAML file: {e}")


def test_contact_form_submission():
    """
    Test contact form submission endpoint
    """
    contact_data = {
        "name": "Test User",
        "email": "test@example.com",
        "message": "Test contact form submission for portfolio"
    }

    response = client.post("/contact", data=contact_data)
    assert response.status_code == 200

    result = response.json()
    assert result['status'] == 'success'
    assert 'message' in result


def test_portfolio_api_endpoint():
    """
    Test the portfolio data API endpoint
    """
    response = client.get("/api/portfolio")
    assert response.status_code == 200

    data = response.json()

    # Basic validation of returned data
    assert 'name' in data
    assert 'projects' in data
    assert 'skills' in data

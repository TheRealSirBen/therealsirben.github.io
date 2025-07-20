import os
import pytest
from fastapi.testclient import TestClient
import yaml

# Import the main application and data loading function
from main import app, load_portfolio_data

# Create a test client
client = TestClient(app)


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


def test_static_files():
    """
    Test availability of key static files
    """
    # Test professional image
    data = load_test_data()
    response = client.get("/static/{}".format(data.get('professionalImage')))
    assert response.status_code == 200

    # Test video source
    response = client.get("/static/{}".format(data.get('personalVideoSrc')))
    assert response.status_code == 200


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

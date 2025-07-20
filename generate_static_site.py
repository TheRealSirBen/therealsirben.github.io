#!/usr/bin/env python3
"""
Static Site Generator for Benedict Dlamini Portfolio
Converts FastAPI app to static HTML for GitHub Pages deployment
"""

import os
import shutil
import yaml
from jinja2 import Environment, FileSystemLoader
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def load_portfolio_data():
    """
    Load portfolio data from YAML file
    """
    yaml_path = os.path.join('data', 'portfolio.yaml')
    try:
        with open(yaml_path, 'r') as file:
            return yaml.safe_load(file)
    except Exception as e:
        logger.error(f"Error loading portfolio data: {e}")
        return {}


def copy_static_files(output_dir):
    """
    Copy all static files to output directory
    """
    static_source = 'static'
    static_dest = os.path.join(output_dir, 'static')

    if os.path.exists(static_source):
        if os.path.exists(static_dest):
            shutil.rmtree(static_dest)
        shutil.copytree(static_source, static_dest)
        logger.info(f"Copied static files from {static_source} to {static_dest}")
    else:
        logger.warning(f"Static directory {static_source} not found")


def create_404_page(output_dir):
    """
    Create a 404.html page for GitHub Pages
    """
    html_404 = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Page Not Found - Benedict Dlamini Portfolio</title>
    <link rel="stylesheet" href="static/css/styles.css">
    <style>
        .error-container {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            min-height: 100vh;
            text-align: center;
            padding: 2rem;
        }
        .error-container h1 {
            font-size: 3rem;
            color: #3498db;
            margin-bottom: 1rem;
        }
        .error-container p {
            font-size: 1.2rem;
            margin-bottom: 2rem;
            color: #666;
        }
        .btn {
            display: inline-block;
            padding: 1rem 2rem;
            background-color: #3498db;
            color: white;
            text-decoration: none;
            border-radius: 5px;
            transition: background-color 0.3s ease;
        }
        .btn:hover {
            background-color: #2980b9;
        }
    </style>
</head>
<body>
    <div class="error-container">
        <h1>404</h1>
        <h2>Page Not Found</h2>
        <p>The page you are looking for might have been moved or doesn't exist.</p>
        <a href="/" class="btn">Return to Home</a>
    </div>
</body>
</html>"""

    with open(os.path.join(output_dir, '404.html'), 'w') as f:
        f.write(html_404)
    logger.info("Created 404.html page")


def generate_static_site():
    """
    Generate static site from FastAPI templates
    """
    # Create output directory
    output_dir = '_site'
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir, exist_ok=True)
    logger.info(f"Created output directory: {output_dir}")

    # Setup Jinja2 environment
    template_dir = 'templates'
    if not os.path.exists(template_dir):
        logger.error(f"Templates directory {template_dir} not found")
        return False

    env = Environment(loader=FileSystemLoader(template_dir))

    # Load portfolio data
    data = load_portfolio_data()
    if not data:
        logger.error("Failed to load portfolio data")
        return False

    try:
        # Render index.html
        template = env.get_template('index.html')
        rendered_html = template.render(data=data)

        # Write rendered HTML
        index_path = os.path.join(output_dir, 'index.html')
        with open(index_path, 'w', encoding='utf-8') as f:
            f.write(rendered_html)
        logger.info(f"Generated index.html at {index_path}")

        # Copy static files
        copy_static_files(output_dir)

        # Create 404 page
        create_404_page(output_dir)

        # Create CNAME file if needed (uncomment and modify if you have a custom domain)
        # with open(os.path.join(output_dir, 'CNAME'), 'w') as f:
        #     f.write('yourdomain.com')

        logger.info("Static site generation completed successfully!")
        return True

    except Exception as e:
        logger.error(f"Error generating static site: {e}")
        return False


if __name__ == '__main__':
    success = generate_static_site()
    if not success:
        exit(1)
    logger.info("Static site ready for deployment!")

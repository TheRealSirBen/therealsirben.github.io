import os
import shutil
import yaml
from jinja2 import Environment, FileSystemLoader
from __init__ import logger


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


def generate_site():
    # Create output directory
    output_dir = '_site'
    os.makedirs(output_dir, exist_ok=True)

    # Setup Jinja2 environment
    env = Environment(loader=FileSystemLoader('templates'))

    # Load portfolio data
    data = load_portfolio_data()

    # Render index.html
    template = env.get_template('index.html')
    rendered_html = template.render(data=data)

    # Write rendered HTML
    with open(os.path.join(output_dir, 'index.html'), 'w') as f:
        f.write(rendered_html)

    # Copy static files
    static_dirs = ['css', 'js', 'images', 'videos']
    for dir_name in static_dirs:
        src_dir = os.path.join('static', dir_name)
        dest_dir = os.path.join(output_dir, 'static', dir_name)

        if os.path.exists(src_dir):
            os.makedirs(dest_dir, exist_ok=True)
            for item in os.listdir(src_dir):
                s = os.path.join(src_dir, item)
                d = os.path.join(dest_dir, item)
                if os.path.isdir(s):
                    shutil.copytree(s, d, dirs_exist_ok=True)
                else:
                    shutil.copy2(s, d)

    # Create 404.html (optional)
    with open(os.path.join(output_dir, '404.html'), 'w') as f:
        f.write("""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>Page Not Found</title>
        </head>
        <body>
            <h1>404 - Page Not Found</h1>
            <p>The page you are looking for does not exist.</p>
            <a href="/">Return to Home</a>
        </body>
        </html>
        """)

    logger.info("Static site generated successfully in '_site' directory")


if __name__ == '__main__':
    generate_site()

# Benedict Dlamini - Professional Portfolio

## Project Overview

A modern, responsive portfolio website showcasing professional projects, skills, and data science expertise.

## Technologies

- FastAPI
- Jinja2 Templating
- GitHub Actions
- GitHub Pages

## Local Development Setup

### Prerequisites

- Python 3.9+
- pip
- virtualenv (recommended)

### Installation Steps

1. Clone the repository

```bash
git clone https://github.com/yourusername/benedict-portfolio.git
cd benedict-portfolio
```

2. Create a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies

```bash
pip install -r requirements.txt
```

4. Run the application

```bash
uvicorn main:app --reload
```

### Running Tests

```bash
pytest tests/
```

## Deployment

### GitHub Pages

This project uses GitHub Actions for deployment to GitHub Pages:

- Pushes to `main` branch trigger automatic deployment
- Static files are prepared and deployed
- Tests are run before deployment

### Manual Deployment

1. Ensure all tests pass
2. Commit and push changes to GitHub
3. GitHub Actions will handle deployment automatically

## Customization

- Update `data/portfolio.yaml` to modify portfolio content
- Adjust `static/` files for custom styling
- Modify `templates/index.html` for layout changes

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

MIT License

## Contact

- Email: thabisaben@gmail.com
- LinkedIn: https://www.linkedin.com/in/benedict-dlamini
- GitHub: https://github.com/TheRealSirBen
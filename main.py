from __init__ import BASE_DIR, logger
from os.path import join, exists
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from yaml import safe_load

# Create FastAPI application
app = FastAPI(
    title="Benedict Dlamini Portfolio",
    description="Personal portfolio showcasing projects and skills",
    version="1.0.0"
)

# Configure static files and templates

app.mount("/static", StaticFiles(directory=join(BASE_DIR, "static")), name="static")
templates = Jinja2Templates(directory=join(BASE_DIR, "templates"))


@app.get("/portfolio.yaml")
async def serve_portfolio_yaml():
    yaml_path = join(BASE_DIR, 'data', 'portfolio.yaml')
    return FileResponse(yaml_path, media_type='text/yaml')


def load_portfolio_data():
    """
    Load portfolio data from YAML file

    Returns:
        Dict containing portfolio information
    """
    yaml_path = join(BASE_DIR, 'data', 'portfolio.yaml')
    try:
        with open(yaml_path, 'r') as file:
            # Use safe_load from PyYAML
            data = safe_load(file)

            # Optional: Add fallback for headline if needed
            if 'strategic_value_proposition' in data:
                data['headline'] = data['strategic_value_proposition'].get('headline', '')

            return data
    except Exception as e:
        logger.error(f"Error loading portfolio data: {e}")
        return {}


class ContactSubmission(BaseModel):
    """
    Pydantic model for contact form submission
    """
    name: str
    email: str
    message: str


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """
    Render the main portfolio page

    Args:
        request: FastAPI Request object

    Returns:
        HTMLResponse with rendered template
    """
    portfolio_data = load_portfolio_data()
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "data": portfolio_data
        }
    )


@app.post("/contact")
async def submit_contact(
        name: str = Form(...),
        email: str = Form(...),
        message: str = Form(...)
):
    """
    Handle contact form submission

    Args:
        name: Sender's name
        email: Sender's email
        message: Message content

    Returns:
        Dict with submission status
    """
    # In a real application, you'd implement actual email sending or database storage
    logger.info(f"Received contact from {name} ({email}): {message}")
    return {
        "status": "success",
        "message": "Your message has been received!"
    }


@app.get("/download/resume")
async def download_resume():
    """
    Serve resume PDF for download

    Returns:
        FileResponse with resume PDF
    """
    resume_path = join(BASE_DIR, "static", "documents", "benedict-dlamini-resume.pdf")

    # In a real app, you'd have an actual resume PDF
    if exists(resume_path):
        return FileResponse(
            resume_path,
            media_type="application/pdf",
            filename="Benedict-Dlamini-Resume.pdf"
        )

    return {"error": "Resume not found"}


# Optional: API endpoint to get portfolio data
@app.get("/api/portfolio")
async def get_portfolio_data():
    """
    Provide portfolio data via API endpoint

    Returns:
        Dict containing portfolio information
    """
    return load_portfolio_data()


# Startup event (optional)
@app.on_event("startup")
async def startup_event():
    """
    Perform startup tasks
    """
    logger.info("Portfolio application starting up!")


# Error handling
@app.exception_handler(404)
async def not_found_handler(request: Request, exc):
    """
    Custom 404 error handler
    """
    return templates.TemplateResponse(
        "error.html",
        {
            "request": request,
            "error_message": "Page not found"
        },
        status_code=404
    )

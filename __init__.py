from os.path import dirname, abspath
from logging import basicConfig, INFO, StreamHandler, getLogger
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = dirname(abspath(__file__))

# Set up logging
basicConfig(
    level=INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[StreamHandler()]
)
logger = getLogger('benedict_dlamini')

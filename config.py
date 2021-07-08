"""Flask configuration variables."""
from os import environ, path, getenv
from dotenv import load_dotenv

# Load environment variables from file .env, stored in this directory.
load_dotenv()


class Config:
    """Set Flask configuration from .env file."""

    # Flask configuration
    FLASK_APP = environ.get('FLASK_APP')
    FLASK_ENV = environ.get('FLASK_ENV')

    SECRET_KEY = environ.get('SECRET_KEY')
    TESTING =  environ.get('TESTING')
    TEST_DATA_PATH = environ.get('TEST_DATA_PATH')


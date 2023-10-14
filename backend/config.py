import os

from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')
DEBUG = os.getenv('DEBUG', 'False') in ('True', '1', 't')
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS').split()
CSRF_TRUSTED_ORIGINS = os.getenv("CSRF_TRUSTED_ORIGINS").split()

DB_HOST = os.getenv('DB_HOST', default='5432')
DB_PORT = os.getenv('DB_PORT', default='db')
DB_NAME = os.getenv('POSTGRES_DB', default='django')
DB_USER = os.getenv('POSTGRES_USER', default='django')
DB_PASS = os.getenv('POSTGRES_PASSWORD', default='')

import os

from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')
DEBUG = os.getenv('DEBUG', 'False') in ('True', '1', 't')
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS').split()

DB_HOST = os.getenv('DB_HOST', default='db')
DB_PORT = os.getenv('DB_PORT', default='5432')
DB_NAME = os.getenv('POSTGRES_DB', default='django')
DB_USER = os.getenv('POSTGRES_USER', default='django')
DB_PASS = os.getenv('POSTGRES_PASSWORD', default='')

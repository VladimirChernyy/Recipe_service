import os

from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')
DEBUG = os.getenv('DEBUG', 'False') in ('True', '1', 't')
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS').split()

DB_HOST = os.getenv('DB_HOST', default='5432')
DB_PORT = os.getenv('DB_PORT', default='db')
DB_NAME = os.getenv('DB_NAME', default='postgres')
DB_USER = os.getenv('DB_USER', default='postgres')
DB_PASS = os.getenv('DB_PASS', default='postgres')

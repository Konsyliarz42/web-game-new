import os
from pathlib import Path

BASE_DIR = Path().absolute()
SECRET_FILE = BASE_DIR.joinpath('secret.txt')
SQLITE_URI = 'sqlite:///' + str(BASE_DIR.joinpath('db.sqlite3'))

class Config():

    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI') or SQLITE_URI
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    if not SECRET_KEY and SECRET_FILE.exists():
        with open(str(SECRET_FILE), 'r') as key:
            SECRET_KEY = key.read()

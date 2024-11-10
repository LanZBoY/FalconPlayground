import os

ENVIRONMENT = os.environ.get("ENV", None)
DB_CONNECTION = os.environ.get("DB_CONNECTION", None)
SECRET = os.environ.get("SECRET", None)
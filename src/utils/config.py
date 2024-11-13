import os

ENVIRONMENT = os.environ.get("ENV", None)
DB_CONNECTION = os.environ.get("DB_CONNECTION", None)
SECRET = os.environ.get("SECRET", None)
CREATE_SECRET = os.environ.get("CREATE_SECRET", None)
REDIS_URL = os.environ.get("REDIS_URL", None)
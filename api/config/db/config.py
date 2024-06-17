from pydantic import BaseModel
# Import the necessary module
from dotenv import load_dotenv
import os

load_dotenv()

class DatabaseConfig(BaseModel):
    dsn: str = os.getenv("SENTRY_DSN", None)
    basedir: str = os.path.abspath(os.path.dirname(__file__))

    env_database_url: str = os.environ.get('DATABASE_URL')
    SQLALCHEMY_DATABASE_URI: str = env_database_url or \
                              'sqlite:///' + os.path.join(basedir, 'app.db')

    if env_database_url is not None:
        env_database_url = env_database_url.replace('+asyncmy', '+pymysql')

    SQLALCHEMY_DATABASE_SYNC_URI: str = env_database_url or \
                                   'sqlite:///' + os.path.join(basedir, 'app.db')

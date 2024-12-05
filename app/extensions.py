import logging
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from redis import Redis

# Initialize Redis connection
try:
    redis_connection = Redis(host='localhost', port=6379)
except Exception as e:
    print(f"Failed to connect to Redis: {e}")
    redis_connection = None

# Initialize shared extensions
db = SQLAlchemy()
migrate = Migrate()
limiter = Limiter(
    key_func=get_remote_address,
    storage_uri="redis://localhost:6379"  # Use Redis as the storage backend
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("app.log"),  # Log to a file
        logging.StreamHandler()         # Log to the console
    ]
)
logger = logging.getLogger(__name__)
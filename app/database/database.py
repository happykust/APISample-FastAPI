import os
import databases
from sqlalchemy import MetaData, create_engine

# Define URL to PostgreSQL database
POSTGRES_URL = 'postgresql://{}:{}@{}:{}/{}'.format(
    os.getenv("POSTGRES_USER"), os.getenv("POSTGRES_PASSWORD"), os.getenv("POSTGRES_HOST"), os.getenv("POSTGRES_PORT"),
    os.getenv("POSTGRES_DB")
)

# Set Metadata for our models
metadata = MetaData()
# Init database for our models
database = databases.Database(POSTGRES_URL)
# Create SQLAlchemy engine for database
engine = create_engine(POSTGRES_URL)

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.proxy import Base as ProxyBase
from models.api_key import Base as ApiKeyBase
from config import DATABASE_URL, DEFAULT_API_KEY
from models.api_key import ApiKey
import secrets

def init_db():
    """
    Initialize the database by creating all necessary tables
    and adding a default API key if one doesn't exist.
    """
    # Create engine
    engine = create_engine(DATABASE_URL)

    # Create all tables
    ProxyBase.metadata.create_all(engine)
    ApiKeyBase.metadata.create_all(engine)

    # Create a session
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        # Check if there's at least one API key
        existing_key = session.query(ApiKey).first()
        if not existing_key:
            # If no API key exists, create one using the DEFAULT_API_KEY from config
            default_key = DEFAULT_API_KEY or secrets.token_urlsafe(32)
            new_api_key = ApiKey(key=default_key, description="Default API Key")
            session.add(new_api_key)
            session.commit()
            print(f"Created default API key: {default_key}")
        else:
            print("Database already contains API key(s). No default key created.")

        print("Database initialized successfully.")
    except Exception as e:
        print(f"An error occurred while initializing the database: {str(e)}")
        session.rollback()
    finally:
        session.close()

if __name__ == "__main__":
    init_db()
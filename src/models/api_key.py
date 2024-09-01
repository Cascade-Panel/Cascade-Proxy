from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class ApiKey(Base):
    """
    Represents an API key in the database.
    """
    __tablename__ = 'api_keys'

    id = Column(Integer, primary_key=True)
    key = Column(String, unique=True, nullable=False)
    description = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    def to_dict(self):
        """
        Convert the ApiKey object to a dictionary.

        Returns:
            dict: A dictionary representation of the ApiKey object.
        """
        return {
            'id': self.id,
            'key': self.key,
            'description': self.description,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat()
        }
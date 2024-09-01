from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Proxy(Base):
    """
    Represents a proxy configuration in the database.
    """
    __tablename__ = 'proxies'

    id = Column(Integer, primary_key=True)
    old_ip = Column(String, nullable=False)
    old_port = Column(Integer, nullable=False)
    new_domain = Column(String, nullable=False)
    https_enabled = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)

    def to_dict(self):
        """
        Convert the Proxy object to a dictionary.

        Returns:
            dict: A dictionary representation of the Proxy object.
        """
        return {
            'id': self.id,
            'old_ip': self.old_ip,
            'old_port': self.old_port,
            'new_domain': self.new_domain,
            'https_enabled': self.https_enabled,
            'is_active': self.is_active
        }
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from python_backend.database import Base

class BrandProfile(Base):
    __tablename__ = "brand_profiles"

    id = Column(Integer, primary_key=True, index=True)

    # The domain this brand belongs to (string name, not FK)
    domain = Column(String, nullable=False)

    # Branding fields
    logo_url = Column(String, nullable=True)
    primary_color = Column(String, nullable=True)
    secondary_color = Column(String, nullable=True)

    # Optional metadata
    created_at = Column(DateTime)

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from python_backend.database import Base

class BulkTape(Base):
    __tablename__ = "bulk_tapes"

    id = Column(Integer, primary_key=True, index=True)
    domain_id = Column(Integer, nullable=False)
    admin_id = Column(Integer, nullable=False)
    filename = Column(String, nullable=False)
    uploaded_at = Column(DateTime)

    properties = relationship("BulkTapeProperty", back_populates="bulk_tape")

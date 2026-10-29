from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from python_backend.database import Base

class BulkTapeProperty(Base):
    __tablename__ = "bulk_tape_properties"

    id = Column(Integer, primary_key=True, index=True)
    bulk_tape_id = Column(Integer, ForeignKey("bulk_tapes.id"))

    raw_data = Column(JSON, nullable=False)
    sanitized_data = Column(JSON, nullable=False)

    property_signal_score = Column(Float, nullable=True)
    accelerated_pass = Column(Integer, nullable=True)

    created_at = Column(DateTime)

    bulk_tape = relationship("BulkTape", back_populates="properties")

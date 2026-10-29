from sqlalchemy import Column, Integer, String, DateTime
from python_backend.database import Base

class Signal(Base):
    __tablename__ = "signals"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    domain_id = Column(Integer, nullable=False)
    type = Column(String, nullable=False)
    message = Column(String, nullable=False)
    created_at = Column(DateTime)

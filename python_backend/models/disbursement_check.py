from sqlalchemy import Column, Integer, Float, DateTime
from python_backend.database import Base

class DisbursementCheck(Base):
    __tablename__ = "disbursement_checks"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    domain_id = Column(Integer, nullable=False)
    amount = Column(Float, nullable=False)
    created_at = Column(DateTime)

from sqlalchemy import Column, Integer, Float, DateTime
from python_backend.database import Base

class LoanEstimate(Base):
    __tablename__ = "loan_estimates"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    domain_id = Column(Integer, nullable=False)
    property_id = Column(Integer, nullable=False)
    loan_amount = Column(Float, nullable=False)
    interest_rate = Column(Float, nullable=False)
    term_months = Column(Integer, nullable=False)
    created_at = Column(DateTime)

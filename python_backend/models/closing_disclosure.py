from sqlalchemy import Column, Integer, Float, DateTime
from python_backend.database import Base

class ClosingDisclosure(Base):
    __tablename__ = "closing_disclosures"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    domain_id = Column(Integer, nullable=False)
    property_id = Column(Integer, nullable=False)
    loan_amount = Column(Float, nullable=False)
    closing_costs = Column(Float, nullable=False)
    cash_to_close = Column(Float, nullable=False)
    created_at = Column(DateTime)

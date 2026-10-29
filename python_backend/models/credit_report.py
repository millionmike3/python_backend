from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey
from python_backend.database import Base

class CreditReportSummary(Base):
    __tablename__ = "credit_report_summaries"

    id = Column(Integer, primary_key=True, index=True)

    borrower_id = Column(Integer, nullable=False)
    application_id = Column(Integer, nullable=False)

    score = Column(Integer, nullable=False)
    utilization = Column(Float, nullable=False)
    derogatories = Column(Integer, nullable=False)
    tradeline_count = Column(Integer, nullable=False)

    credit_signal_score = Column(Float, nullable=True)

    created_at = Column(DateTime)

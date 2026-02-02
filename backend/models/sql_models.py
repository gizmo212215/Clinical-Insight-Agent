from sqlalchemy import Column, String, Date, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()


class ClinicalTrial(Base):
    __tablename__ = "clinical_trials"
    nct_id = Column(String, primary_key=True, index=True)
    title = Column(Text, nullable=False)
    organization = Column(String, nullable=True)
    status = Column(String, nullable=True)
    study_type = Column(String, nullable=True)
    phases = Column(String, nullable=True)
    start_date = Column(Date, nullable=True)
    completion_date = Column(Date, nullable=True)
    last_update_posted = Column(Date, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<ClinicalTrial(nct_id={self.nct_id}, title={self.title})>"

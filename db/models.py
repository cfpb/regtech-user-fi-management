
from sqlalchemy import Column, DateTime, ForeignKeyConstraint, Index, PrimaryKeyConstraint, String
from sqlalchemy.sql import func
from db.database import Base

class Financial_Institutions(Base):
    __tablename__ = 'financial_institutions'
    lei = Column(String, nullable=False)
    name = Column(String, nullable=False)
    event_time  = Column(DateTime(timezone=True), server_default=func.now())
    __table_args__ = (
       PrimaryKeyConstraint("lei", name="financial_institutions_pkey"),
       Index('ix_financial_institutions_lei', "lei", postgresql_using='gin', unique=True),
       Index('ix_financial_institutions_name', "name", postgresql_using='gin'),
       {"schema": "fi"}
       )
    
class Financial_Institutions_Domains(Base):
    __tablename__ = 'financial_institutions_domains'
    domain = Column(String, nullable=False)
    lei = Column(String, nullable=False)
    event_time  = Column(DateTime(timezone=True), server_default=func.now())
    __table_args__ = (
       PrimaryKeyConstraint("domain", "lei", name="financial_institution_domains_pkey"),
       Index('ix_financial_institution_domains_domain', "domain", postgresql_using='gin'),
       Index('ix_financial_institution_domains_lei', "lei", postgresql_using='gin'),
       ForeignKeyConstraint(["lei"], ["financial_institutions.lei"]),
       {"schema": "fi"}
       )
    
class Denied_Domains(Base):
    __tablename__ = 'denied_domains'
    domain = Column(String, nullable=False)
    event_time  = Column(DateTime(timezone=True), server_default=func.now())
    __table_args__ = (
       PrimaryKeyConstraint("domain", name="denied_domains_pkey"),
       Index('ix_denied_domains_domain', "domain", postgresql_using='gin', unique=True),
       {"schema": "fi"}
       )

    
    
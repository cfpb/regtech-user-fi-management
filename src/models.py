from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, DateTime, ForeignKey, Index, Integer, PrimaryKeyConstraint, String
from sqlalchemy.sql import func

Base = declarative_base()
metadata = Base.metadata


class Financial_Institutions(Base):
    __tablename__ = 'financial_institutions'
    lei = Column(String, nullable=False)
    name = Column(String, nullable=False)
    event_time  = Column(DateTime(timezone=True), server_default=func.now())
    __table_args__ = (
       PrimaryKeyConstraint("lei", name="financial_institutions_pkey"),
       Index('ix_financial_institutions_lei', "lei", unique=True),
       Index('ix_financial_institutions_name', "name"),
       )
    def __repr__(self):
        return f"lei: {self.lei}, name: {self.name}"
    
class Financial_Institutions_Domains(Base):
    __tablename__ = 'financial_institutions_domains'
    domain = Column(String, nullable=False)
    lei = Column(String, ForeignKey("financial_institutions.lei"))
    event_time  = Column(DateTime(timezone=True), server_default=func.now())
    __table_args__ = (
       PrimaryKeyConstraint("domain", "lei", name="financial_institution_domains_pkey"),
       Index('ix_financial_institution_domains_domain', "domain"),
       Index('ix_financial_institution_domains_lei', "lei"),
   
       )
    def __repr__(self):
        return f"lei: {self.lei}, domain: {self.domain}"
    
class Denied_Domains(Base):
    __tablename__ = 'denied_domains'
    domain = Column(String, nullable=False)
    event_time  = Column(DateTime(timezone=True), server_default=func.now())
    __table_args__ = (
       PrimaryKeyConstraint("domain", name="denied_domains_pkey"),
       Index('ix_denied_domains_domain', "domain", unique=True)
     
       )
    def __repr__(self):
        return f"domain: {self.domain}"
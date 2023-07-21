from datetime import datetime
from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from . import Base


class AuditMixin(object):
    event_time: Mapped[datetime] = mapped_column(server_default=func.now())


class FinancialInstitutionDao(AuditMixin, Base):
    __tablename__ = "financial_institutions"
    lei: Mapped[str] = mapped_column(unique=True, index=True, primary_key=True)
    name: Mapped[str] = mapped_column(index=True)
    domains = relationship("FinancialInstitutionDomainDao", back_populates="fi")


class FinancialInstitutionDomainDao(AuditMixin, Base):
    __tablename__ = "financial_institution_domains"
    domain: Mapped[str] = mapped_column(index=True, primary_key=True)
    lei: Mapped[str] = mapped_column(
        ForeignKey("financial_institutions.lei"), index=True, primary_key=True
    )
    fi = relationship("FinancialInstitutionDao", back_populates="domains")

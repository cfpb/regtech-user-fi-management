from datetime import datetime
from typing import List
from sqlalchemy import ForeignKey, func, String, inspect
from sqlalchemy.orm import Mapped, mapped_column, relationship, DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncAttrs


class Base(AsyncAttrs, DeclarativeBase):
    pass


class AuditMixin(object):
    event_time: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())


class SblTypeMappingDao(Base):
    __tablename__ = "fi_to_type_mapping"
    version: Mapped[int] = mapped_column(nullable=False, default=0)
    __mapper_args__ = {"version_id_col": version, "version_id_generator": False}
    lei: Mapped[str] = mapped_column("fi_id", ForeignKey("financial_institutions.lei"), primary_key=True)
    type_id: Mapped[str] = mapped_column(ForeignKey("sbl_institution_type.id"), primary_key=True)
    sbl_type: Mapped["SBLInstitutionTypeDao"] = relationship(lazy="selectin")
    details: Mapped[str] = mapped_column(nullable=True)
    modified_by: Mapped[str] = mapped_column()

    def __eq__(self, other: "SblTypeMappingDao") -> bool:
        return self.lei == other.lei and self.type_id == other.type_id and self.details == other.details

    def __hash__(self) -> int:
        return hash((self.lei, self.type_id, self.details))

    def as_db_dict(self):
        data = {}
        for attr, column in inspect(self.__class__).c.items():
            data[column.name] = getattr(self, attr)
        return data


class FinancialInstitutionDao(AuditMixin, Base):
    __tablename__ = "financial_institutions"
    version: Mapped[int] = mapped_column(nullable=False, default=0)
    __mapper_args__ = {"version_id_col": version, "version_id_generator": False}
    lei: Mapped[str] = mapped_column(String(20), unique=True, index=True, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), index=True)
    is_active: Mapped[bool] = mapped_column(index=True)
    domains: Mapped[List["FinancialInstitutionDomainDao"]] = relationship(
        "FinancialInstitutionDomainDao", back_populates="fi", lazy="selectin"
    )
    tax_id: Mapped[str] = mapped_column(String(10), unique=True, nullable=True)
    rssd_id: Mapped[int] = mapped_column(unique=True, nullable=True)
    primary_federal_regulator_id: Mapped[str] = mapped_column(ForeignKey("federal_regulator.id"), nullable=True)
    primary_federal_regulator: Mapped["FederalRegulatorDao"] = relationship(lazy="selectin")
    hmda_institution_type_id: Mapped[str] = mapped_column(ForeignKey("hmda_institution_type.id"), nullable=True)
    hmda_institution_type: Mapped["HMDAInstitutionTypeDao"] = relationship(lazy="selectin")
    sbl_institution_types: Mapped[List[SblTypeMappingDao]] = relationship(lazy="selectin", cascade="all, delete-orphan")
    hq_address_street_1: Mapped[str] = mapped_column(String(255))
    hq_address_street_2: Mapped[str] = mapped_column(String(255), nullable=True)
    hq_address_street_3: Mapped[str] = mapped_column(String(255), nullable=True)
    hq_address_street_4: Mapped[str] = mapped_column(String(255), nullable=True)
    hq_address_city: Mapped[str] = mapped_column(String(255))
    hq_address_state_code: Mapped[str] = mapped_column(ForeignKey("address_state.code"), nullable=True)
    hq_address_state: Mapped["AddressStateDao"] = relationship(lazy="selectin")
    hq_address_zip: Mapped[str] = mapped_column(String(5))
    parent_lei: Mapped[str] = mapped_column(String(20), nullable=True)
    parent_legal_name: Mapped[str] = mapped_column(String(255), nullable=True)
    parent_rssd_id: Mapped[int] = mapped_column(nullable=True)
    top_holder_lei: Mapped[str] = mapped_column(String(20), nullable=True)
    top_holder_legal_name: Mapped[str] = mapped_column(String(255), nullable=True)
    top_holder_rssd_id: Mapped[int] = mapped_column(nullable=True)
    modified_by: Mapped[str] = mapped_column()


class FinancialInstitutionDomainDao(AuditMixin, Base):
    __tablename__ = "financial_institution_domains"
    domain: Mapped[str] = mapped_column(index=True, primary_key=True)
    lei: Mapped[str] = mapped_column(ForeignKey("financial_institutions.lei"), index=True, primary_key=True)
    fi: Mapped["FinancialInstitutionDao"] = relationship("FinancialInstitutionDao", back_populates="domains")


class DeniedDomainDao(AuditMixin, Base):
    __tablename__ = "denied_domains"
    domain: Mapped[str] = mapped_column(index=True, primary_key=True)


class FederalRegulatorDao(AuditMixin, Base):
    __tablename__ = "federal_regulator"
    id: Mapped[str] = mapped_column(String(4), index=True, primary_key=True, unique=True)
    name: Mapped[str] = mapped_column(unique=True, nullable=False)


class InstitutionTypeMixin(AuditMixin):
    id: Mapped[str] = mapped_column(index=True, primary_key=True, unique=True)
    name: Mapped[str] = mapped_column(unique=True)


class HMDAInstitutionTypeDao(InstitutionTypeMixin, Base):
    __tablename__ = "hmda_institution_type"


class SBLInstitutionTypeDao(InstitutionTypeMixin, Base):
    __tablename__ = "sbl_institution_type"


class AddressStateDao(AuditMixin, Base):
    __tablename__ = "address_state"
    code: Mapped[str] = mapped_column(String(2), index=True, primary_key=True, unique=True)
    name: Mapped[str] = mapped_column(unique=True, nullable=False)

from typing import List
from pydantic import BaseModel


class FinancialInsitutionDomainBase(BaseModel):
    domain: str


class FinancialInsitutionDomainCreate(FinancialInsitutionDomainBase):
    pass


class FinancialInsitutionDomainDto(FinancialInsitutionDomainBase):
    lei: str

    class Config:
        orm_mode = True


class FinancialInstitutionBase(BaseModel):
    name: str


class FinancialInstitutionDto(FinancialInstitutionBase):
    lei: str

    class Config:
        orm_mode = True


class FinancialInstitutionWithDomainsDto(FinancialInstitutionDto):
    domains: List[FinancialInsitutionDomainDto] = []


class DeniedDomainDto(BaseModel):
    domain: str

    class Config:
        orm_mode = True

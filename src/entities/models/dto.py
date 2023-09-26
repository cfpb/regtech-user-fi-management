from typing import List, Dict, Any, Set
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


class UserProfile(BaseModel):
    firstName: str
    lastName: str
    leis: Set[str] = None

    def get_user(self) -> Dict[str, Any]:
        return {"firstName": self.firstName, "lastName": self.lastName}

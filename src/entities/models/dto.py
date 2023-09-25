from typing import Any, Dict, List

from pydantic import BaseModel
from starlette.authentication import BaseUser


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


class AuthenticatedUser(BaseUser, BaseModel):
    claims: Dict[str, Any]
    name: str
    username: str
    email: str
    id: str
    institutions: List[str]

    @classmethod
    def from_claim(cls, claims: Dict[str, Any]) -> "AuthenticatedUser":
        return cls(
            claims=claims,
            name=claims.get("name", ""),
            username=claims.get("preferred_username", ""),
            email=claims.get("email", ""),
            id=claims.get("sub", ""),
            institutions=cls.parse_institutions(claims.get("institutions")),
        )

    @classmethod
    def parse_institutions(cls, institutions: List[str] | None) -> List[str]:
        """
        Parse out the list of institutions returned by Keycloak

        Args:
            institutions(List[str]): list of full institution paths provided by keycloak,
            it is possible to have nested paths, though we may not use the feature.
            e.g. ["/ROOT_INSTITUTION/CHILD_INSTITUTION/GRAND_CHILD_INSTITUTION"]

        Returns:
            List[str]: List of cleaned up institutions.
            e.g. ["GRAND_CHILD_INSTITUTION"]
        """
        if institutions:
            return [institution.split("/")[-1] for institution in institutions]
        else:
            return []

    @property
    def is_authenticated(self) -> bool:
        return True

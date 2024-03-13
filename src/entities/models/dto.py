import re

from typing import Generic, List, Set, Sequence
from pydantic import BaseModel, model_validator
from typing import TypeVar

T = TypeVar("T")


class VersionedData(BaseModel, Generic[T]):
    version: int
    data: T


class FinancialInsitutionDomainBase(BaseModel):
    domain: str


class FinancialInsitutionDomainCreate(FinancialInsitutionDomainBase):
    pass


class FinancialInsitutionDomainDto(FinancialInsitutionDomainBase):
    lei: str

    class Config:
        from_attributes = True


class FinancialInstitutionBase(BaseModel):
    lei: str
    name: str
    is_active: bool


class SblTypeAssociationDto(BaseModel):
    id: str
    details: str | None = None

    @model_validator(mode="after")
    def validate_type(self) -> "SblTypeAssociationDto":
        """
        Validates `Other` type and free form input.
        If `Other` is selected, then details should be filled in;
        vice versa if `Other` is not selected, then details should be null.
        """
        other_type_id = "13"
        if self.id == other_type_id and not self.details:
            raise ValueError(f"SBL institution type '{other_type_id}' requires additional details.")
        elif self.id != other_type_id:
            self.details = None
        return self

    class Config:
        from_attributes = True


class SblTypeAssociationPatchDto(BaseModel):
    sbl_institution_types: Sequence[SblTypeAssociationDto | str]


class FinancialInstitutionDto(FinancialInstitutionBase):
    tax_id: str | None = None
    rssd_id: int | None = None
    primary_federal_regulator_id: str | None = None
    hmda_institution_type_id: str | None = None
    sbl_institution_types: List[SblTypeAssociationDto | str] = []
    hq_address_street_1: str
    hq_address_street_2: str | None = None
    hq_address_city: str
    hq_address_state_code: str
    hq_address_zip: str
    parent_lei: str | None = None
    parent_legal_name: str | None = None
    parent_rssd_id: int | None = None
    top_holder_lei: str | None = None
    top_holder_legal_name: str | None = None
    top_holder_rssd_id: int | None = None
    version: int | None = None

    @model_validator(mode="after")
    def validate_fi(self) -> "FinancialInstitutionDto":
        if self.tax_id:
            match = re.match(r"^([0-9]{2}-[0-9]{7})", self.tax_id)
            if not match:
                raise ValueError(
                    f"Invalid tax_id {self.tax_id}. FinancialInstitution tax_id must conform to XX-XXXXXXX pattern."
                )
        return self

    class Config:
        from_attributes = True


class DeniedDomainDto(BaseModel):
    domain: str

    class Config:
        from_attributes = True


class UserProfile(BaseModel):
    first_name: str
    last_name: str
    leis: Set[str] | None = None

    def to_keycloak_user(self):
        return {"firstName": self.first_name, "lastName": self.last_name}


class FederalRegulatorBase(BaseModel):
    id: str


class FederalRegulatorDto(FederalRegulatorBase):
    name: str

    class Config:
        from_attributes = True


class InstitutionTypeDto(BaseModel):
    id: str
    name: str

    class Config:
        from_attributes = True


class SblTypeAssociationDetailsDto(BaseModel):
    sbl_type: InstitutionTypeDto
    details: str | None = None

    class Config:
        from_attributes = True


class AddressStateBase(BaseModel):
    code: str


class AddressStateDto(AddressStateBase):
    name: str

    class Config:
        from_attributes = True


class FinancialInstitutionWithRelationsDto(FinancialInstitutionDto):
    primary_federal_regulator: FederalRegulatorDto | None = None
    hmda_institution_type: InstitutionTypeDto | None = None
    sbl_institution_types: List[SblTypeAssociationDetailsDto] = []
    hq_address_state: AddressStateDto
    domains: List[FinancialInsitutionDomainDto] = []


class FinancialInstitutionAssociationDto(FinancialInstitutionWithRelationsDto):
    approved: bool

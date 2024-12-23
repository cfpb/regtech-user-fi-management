from typing import Sequence, TypeVar
from regtech_user_fi_management.entities.models.dao import Base, SblTypeMappingDao
from regtech_user_fi_management.entities.models.dto import SblTypeAssociationDto

T = TypeVar("T", bound=Base)


def get_associated_sbl_types(
    lei: str, user_id: str, types: Sequence[SblTypeAssociationDto | str]
) -> Sequence[SblTypeMappingDao]:
    return [
        (
            SblTypeMappingDao(type_id=t, lei=lei, modified_by=user_id)
            if isinstance(t, str)
            else SblTypeMappingDao(type_id=t.id, details=t.details, lei=lei, modified_by=user_id)
        )
        for t in types
    ]

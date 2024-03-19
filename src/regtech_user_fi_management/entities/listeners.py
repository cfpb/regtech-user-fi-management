from typing import List
from sqlalchemy import Connection, Table, event, inspect
from sqlalchemy.orm import Mapper

from regtech_user_fi_management.entities.models.dao import Base, FinancialInstitutionDao, SblTypeMappingDao
from regtech_user_fi_management.entities.engine.engine import engine


def inspect_fi(fi: FinancialInstitutionDao):
    changes = {}
    new_version = fi.version + 1 if fi.version else 1
    state = inspect(fi)
    for attr in state.attrs:
        if attr.key == "event_time":
            continue
        if attr.key == "sbl_institution_types":
            field_changes = inspect_type_fields(attr.value)
            if attr.history.has_changes() or field_changes:
                old_types = {"old": [o.as_db_dict() for o in attr.history.deleted]} if attr.history.deleted else {}
                new_types = (
                    {"new": [{**n.as_db_dict(), "version": new_version} for n in attr.history.added]}
                    if attr.history.added
                    else {}
                )
                changes[attr.key] = {**old_types, **new_types, "field_changes": field_changes}
        elif attr.history.has_changes():
            changes[attr.key] = {"old": attr.history.deleted, "new": attr.history.added}
    return changes


def inspect_type_fields(types: List[SblTypeMappingDao], fields: List[str] = ["details"]):
    changes = []
    for t in types:
        state = inspect(t)
        attr_changes = {
            attr.key: {"old": attr.history.deleted, "new": attr.history.added}
            for attr in state.attrs
            if attr.key in fields and attr.history.has_changes()
        }
        if attr_changes:
            changes.append({**t.as_db_dict(), **attr_changes})
    return changes


def _setup_fi_history(fi_history: Table, mapping_history: Table):
    def _insert_history(
        mapper: Mapper[FinancialInstitutionDao], connection: Connection, target: FinancialInstitutionDao
    ):
        new_version = target.version + 1 if target.version else 1
        changes = inspect_fi(target)
        if changes:
            target.version = new_version
            for t in target.sbl_institution_types:
                t.version = new_version
            hist = target.__dict__.copy()
            hist.pop("event_time", None)
            history_columns = fi_history.columns.keys()
            for key in hist.copy():
                if key not in history_columns:
                    del hist[key]
            hist["changeset"] = changes
            types = [t.as_db_dict() for t in target.sbl_institution_types]
            connection.execute(fi_history.insert().values(hist))
            if types:
                connection.execute(mapping_history.insert().values(types))

    return _insert_history


async def setup_dao_listeners():
    async with engine.begin() as connection:
        fi_history, mapping_history = await connection.run_sync(
            lambda conn: (
                Table("financial_institutions_history", Base.metadata, autoload_with=conn),
                Table("fi_to_type_mapping_history", Base.metadata, autoload_with=conn),
            )
        )

    insert_fi_history = _setup_fi_history(fi_history, mapping_history)

    event.listen(FinancialInstitutionDao, "before_insert", insert_fi_history)
    event.listen(FinancialInstitutionDao, "before_update", insert_fi_history)

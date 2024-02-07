from sqlalchemy import Connection, Table, event, inspect
from sqlalchemy.orm import Mapper

from .models.dao import Base, FinancialInstitutionDao
from entities.engine.engine import engine


def _setup_fi_history(fi_history: Table, mapping_history: Table):
    def _insert_history(
        mapper: Mapper[FinancialInstitutionDao], connection: Connection, target: FinancialInstitutionDao
    ):
        new_version = target.version + 1 if target.version else 1
        changes = {}
        state = inspect(target)
        for attr in state.attrs:
            if attr.key == "event_time":
                continue
            attr_hist = attr.load_history()
            if not attr_hist.has_changes():
                continue
            if attr.key == "sbl_institution_types":
                old_types = [o.as_db_dict() for o in attr_hist.deleted]
                new_types = [{**n.as_db_dict(), "version": new_version} for n in attr_hist.added]
                changes[attr.key] = {"old": old_types, "new": new_types}
            else:
                changes[attr.key] = {"old": attr_hist.deleted, "new": attr_hist.added}
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

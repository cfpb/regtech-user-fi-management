from alembic import op
from sqlalchemy import engine_from_config
import sqlalchemy
from csv import DictReader
import os


def table_exists(table_name):
    config = op.get_context().config
    engine = config.attributes.get("connection", None)
    if engine is None:
        engine = engine_from_config(config.get_section(config.config_ini_section), prefix="sqlalchemy.")
    inspector = sqlalchemy.inspect(engine)
    tables = inspector.get_table_names()
    return table_name in tables


def get_feed_data_from_file(table_name):
    file_dir = os.path.dirname(os.path.realpath(__file__))
    data_file_path = f"{file_dir}/feed/%s.csv" % table_name
    data_file = open(data_file_path, "r")
    reader = DictReader(data_file, delimiter="|")
    output_list = list()
    for dictionary in reader:
        output_list.append(dictionary)
    return output_list

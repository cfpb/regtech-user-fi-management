import pytest
from config import Settings


def test_postgres_dsn_building():
    mock_config = {
        "inst_db_name": "test",
        "inst_db_user": "user",
        "inst_db_pwd": "\\z9-/tgb76#@",
        "inst_db_host": "test:5432",
        "inst_db_scehma": "test",
    }
    settings = Settings(**mock_config)
    assert str(settings.inst_conn) == "postgresql+asyncpg://user:%5Cz9-%2Ftgb76%23%40@test:5432/test"


def test_jwt_opts_valid_values():
    mock_config = {
        "jwt_opts_test1": "true",
        "jwt_opts_test2": "true",
        "jwt_opts_test3": "12",
    }
    settings = Settings(**mock_config)
    assert settings.jwt_opts == {"test1": True, "test2": True, "test3": 12}


def test_jwt_opts_invalid_values():
    mock_config = {
        "jwt_opts_test1": "not a bool or int",
        "jwt_opts_test2": "true",
        "jwt_opts_test3": "12",
    }
    with pytest.raises(Exception) as e:
        Settings(**mock_config)
    assert "validation error" in str(e.value)

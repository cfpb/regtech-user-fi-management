from regtech_user_fi_management.config import Settings


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


def test_default_server_configs():
    settings = Settings()
    assert settings.server_config.host == "0.0.0.0"
    assert settings.server_config.workers == 4
    assert settings.server_config.reload is False
    assert settings.server_config.time_out == 65
    assert settings.server_config.port == 8888

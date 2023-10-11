import pytest
from config import Settings


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

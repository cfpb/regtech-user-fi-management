import pytest
from oauth2.oauth2_admin import get_jwt_opts


class TestOauth2Admin:
    def test_empty_jwt_opts(self):
        assert get_jwt_opts("") == {}

    def test_valid_values(self):
        assert get_jwt_opts("key1:True,key2:False,key3:1") == {"key1": True, "key2": False, "key3": 1}

    def test_invalid_jwt_opts(self):
        with pytest.raises(Exception) as e:
            get_jwt_opts("key1:true")
        assert "malformed node or string" in str(e.value).lower()

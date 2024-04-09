from copy import deepcopy
import pytest
from unittest.mock import Mock, call
from pytest_mock import MockerFixture

from sqlalchemy import Connection, Insert, Table
from sqlalchemy.orm import Mapper, InstanceState, AttributeState
from sqlalchemy.orm.attributes import History

from regtech_user_fi_management.entities.models.dao import (
    FinancialInstitutionDao,
    SBLInstitutionTypeDao,
    SblTypeMappingDao,
)

from regtech_user_fi_management.entities.listeners import _setup_fi_history


class TestListeners:
    fi_history: Table = Mock(Table)
    mapping_history: Table = Mock(Table)
    mapper: Mapper = Mock(Mapper)
    connection: Connection = Mock(Connection)
    target: FinancialInstitutionDao = FinancialInstitutionDao(
        name="Test Bank 123",
        lei="TESTBANK123",
        is_active=True,
        tax_id="12-3456789",
        rssd_id=1234,
        primary_federal_regulator_id="FRI1",
        hmda_institution_type_id="HIT1",
        sbl_institution_types=[SblTypeMappingDao(sbl_type=SBLInstitutionTypeDao(id="SIT1", name="SIT1"))],
        hq_address_street_1="Test Address Street 1",
        hq_address_street_2="",
        hq_address_street_3="",
        hq_address_street_4="",
        hq_address_city="Test City 1",
        hq_address_state_code="GA",
        hq_address_zip="00000",
        parent_lei="PARENTTESTBANK123",
        parent_legal_name="PARENT TEST BANK 123",
        parent_rssd_id=12345,
        top_holder_lei="TOPHOLDERLEI123",
        top_holder_legal_name="TOP HOLDER LEI 123",
        top_holder_rssd_id=123456,
        modified_by="test_user_id",
    )

    @pytest.fixture(autouse=True)
    def setup(self):
        self.fi_history.reset_mock()
        self.fi_history.columns = {"name": "test"}
        self.mapping_history.reset_mock()
        self.mapper.reset_mock()
        self.connection.reset_mock()

    def test_fi_history_listener(self, mocker: MockerFixture):
        inspect_mock = mocker.patch("regtech_user_fi_management.entities.listeners.inspect")
        attr_mock1: AttributeState = Mock(AttributeState)
        attr_mock1.key = "name"
        attr_mock2: AttributeState = Mock(AttributeState)
        attr_mock2.key = "event_time"
        state_mock: InstanceState = Mock(InstanceState)
        state_mock.attrs = [attr_mock1, attr_mock2]
        inspect_mock.return_value = state_mock
        fi_listener = _setup_fi_history(self.fi_history, self.mapping_history)
        fi_listener(self.mapper, self.connection, self.target)
        inspect_mock.assert_called_once_with(self.target)
        self.fi_history.insert.assert_called_once()
        self.mapping_history.insert.assert_called_once()

    def test_fi_history_listener_no_types(self, mocker: MockerFixture):
        inspect_mock = mocker.patch("regtech_user_fi_management.entities.listeners.inspect")
        attr_mock1: AttributeState = Mock(AttributeState)
        attr_mock1.key = "name"
        attr_mock2: AttributeState = Mock(AttributeState)
        attr_mock2.key = "event_time"
        state_mock: InstanceState = Mock(InstanceState)
        state_mock.attrs = [attr_mock1, attr_mock2]
        inspect_mock.return_value = state_mock
        fi_listener = _setup_fi_history(self.fi_history, self.mapping_history)
        no_types = deepcopy(self.target)
        no_types.sbl_institution_types = []
        fi_listener(self.mapper, self.connection, no_types)
        inspect_mock.assert_called_once_with(no_types)
        self.fi_history.insert.assert_called_once()
        self.mapping_history.insert.assert_not_called()

    def _get_fi_inspect_mock(self):
        fi_attr_mock: AttributeState = Mock(AttributeState)
        fi_attr_mock.key = "sbl_institution_types"
        fi_attr_mock.value = self.target.sbl_institution_types
        fi_attr_mock.history = History(added=[], deleted=[], unchanged=[])
        fi_state_mock: InstanceState = Mock(InstanceState)
        fi_state_mock.attrs = [fi_attr_mock]
        return fi_state_mock

    def _get_mapping_inspect_mock(self):
        mapping_attr_mock: AttributeState = Mock(AttributeState)
        mapping_attr_mock.key = "details"
        mapping_attr_mock.history = History(added=["new type"], deleted=["old type"], unchanged=[])
        mapping_state_mock: InstanceState = Mock(InstanceState)
        mapping_state_mock.attrs = [mapping_attr_mock]
        return mapping_state_mock

    def test_fi_mapping_changed(self, mocker: MockerFixture):
        inspect_mock = mocker.patch("regtech_user_fi_management.entities.listeners.inspect")
        fi_state_mock = self._get_fi_inspect_mock()
        mapping_state_mock = self._get_mapping_inspect_mock()

        def inspect_side_effect(inspect_target):
            if inspect_target == self.target:
                return fi_state_mock
            elif inspect_target == self.target.sbl_institution_types[0]:
                return mapping_state_mock

        inspect_mock.side_effect = inspect_side_effect
        fi_insert_mock = Mock(Insert)
        self.fi_history.insert.return_value = fi_insert_mock
        mapping_insert_mock = Mock(Insert)
        self.mapping_history.insert.return_value = mapping_insert_mock
        fi_listener = _setup_fi_history(self.fi_history, self.mapping_history)
        fi_listener(self.mapper, self.connection, self.target)
        inspect_mock.assert_has_calls([call(self.target), call(self.target.sbl_institution_types[0])])
        self.fi_history.insert.assert_called_once()
        self.mapping_history.insert.assert_called_once()
        fi_insert_mock.values.assert_called_once()
        args, _ = fi_insert_mock.values.call_args
        insert_data = args[0]
        assert insert_data["changeset"]["sbl_institution_types"]["field_changes"][0]["details"] == {
            "old": ["old type"],
            "new": ["new type"],
        }

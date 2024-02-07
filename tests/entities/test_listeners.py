from unittest.mock import Mock
from pytest_mock import MockerFixture

from sqlalchemy import Connection, Table
from sqlalchemy.orm import Mapper, InstanceState, AttributeState

from entities.models.dao import FinancialInstitutionDao, SBLInstitutionTypeDao, SblTypeMappingDao

from entities.listeners import _setup_fi_history


class TestListeners:
    fi_history: Table = Mock(Table)
    mapping_history: Table = Mock(Table)
    mapper: Mapper = Mock(Mapper)
    connection: Connection = Mock(Connection)
    target: FinancialInstitutionDao = FinancialInstitutionDao(
        name="Test Bank 123",
        lei="TESTBANK123",
        is_active=True,
        tax_id="123456789",
        rssd_id=1234,
        primary_federal_regulator_id="FRI1",
        hmda_institution_type_id="HIT1",
        sbl_institution_types=[SblTypeMappingDao(sbl_type=SBLInstitutionTypeDao(id="SIT1", name="SIT1"))],
        hq_address_street_1="Test Address Street 1",
        hq_address_street_2="",
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

    def test_fi_history_listener(self, mocker: MockerFixture):
        inspect_mock = mocker.patch("entities.listeners.inspect")
        attr_mock1: AttributeState = Mock(AttributeState)
        attr_mock1.key = "name"
        attr_mock2: AttributeState = Mock(AttributeState)
        attr_mock2.key = "event_time"
        state_mock: InstanceState = Mock(InstanceState)
        state_mock.attrs = [attr_mock1, attr_mock2]
        self.fi_history.columns = {"name": "test"}
        inspect_mock.return_value = state_mock
        fi_listener = _setup_fi_history(self.fi_history, self.mapping_history)
        fi_listener(self.mapper, self.connection, self.target)
        inspect_mock.assert_called_once_with(self.target)
        attr_mock1.load_history.assert_called_once()
        self.fi_history.insert.assert_called_once()

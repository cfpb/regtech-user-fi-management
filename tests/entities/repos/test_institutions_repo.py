import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from entities.models import (
    FinancialInstitutionDao,
    FinancialInstitutionDomainDao,
    FinancialInsitutionDomainCreate,
)
from entities.models import DeniedDomainDao
from entities.repos import institutions_repo as repo


class TestInstitutionsRepo:
    @pytest.fixture(scope="function", autouse=True)
    async def setup(
        self,
        transaction_session: AsyncSession,
    ):
        fi_dao_123, fi_dao_456, fi_dao_sub_456 = (
            FinancialInstitutionDao(
                name="Test Bank 123",
                lei="TESTBANK123",
                domains=[FinancialInstitutionDomainDao(domain="test.bank.1", lei="TESTBANK123")],
            ),
            FinancialInstitutionDao(
                name="Test Bank 456",
                lei="TESTBANK456",
                domains=[FinancialInstitutionDomainDao(domain="test.bank.2", lei="TESTBANK456")],
            ),
            FinancialInstitutionDao(
                name="Test Sub Bank 456",
                lei="TESTSUBBANK456",
                domains=[FinancialInstitutionDomainDao(domain="sub.test.bank.2", lei="TESTSUBBANK456")],
            ),
        )
        transaction_session.add(fi_dao_123)
        transaction_session.add(fi_dao_456)
        transaction_session.add(fi_dao_sub_456)
        await transaction_session.commit()

    async def test_get_institutions(self, query_session: AsyncSession):
        res = await repo.get_institutions(query_session)
        assert len(res) == 3

    async def test_get_institutions_by_domain(self, query_session: AsyncSession):
        # verify 'generic' domain queries don't work
        res = await repo.get_institutions(query_session, domain="bank")
        assert len(res) == 0

        res = await repo.get_institutions(query_session, domain="test.bank.1")
        assert len(res) == 1

        # shouldn't find sub.test.bank.2
        res = await repo.get_institutions(query_session, domain="test.bank.2")
        assert len(res) == 1

        res = await repo.get_institutions(query_session, domain="sub.test.bank.2")
        assert len(res) == 1

    async def test_get_institutions_by_domain_not_existing(self, query_session: AsyncSession):
        res = await repo.get_institutions(query_session, domain="testing.bank")
        assert len(res) == 0

    async def test_get_institutions_by_lei_list(self, query_session: AsyncSession):
        res = await repo.get_institutions(query_session, leis=["TESTBANK123", "TESTBANK456"])
        assert len(res) == 2

    async def test_get_institutions_by_lei_list_item_not_existing(self, query_session: AsyncSession):
        res = await repo.get_institutions(query_session, leis=["NOTTESTBANK"])
        assert len(res) == 0

    async def test_add_institution(self, transaction_session: AsyncSession):
        await repo.upsert_institution(
            transaction_session,
            FinancialInstitutionDao(name="New Bank 123", lei="NEWBANK123"),
        )
        res = await repo.get_institutions(transaction_session)
        assert len(res) == 4

    async def test_update_institution(self, transaction_session: AsyncSession):
        await repo.upsert_institution(
            transaction_session,
            FinancialInstitutionDao(name="Test Bank 234", lei="TESTBANK123"),
        )
        res = await repo.get_institutions(transaction_session)
        assert len(res) == 3
        assert res[0].name == "Test Bank 234"

    async def test_add_domains(self, transaction_session: AsyncSession, query_session: AsyncSession):
        await repo.add_domains(
            transaction_session,
            "TESTBANK123",
            [FinancialInsitutionDomainCreate(domain="bank.test")],
        )
        fi = await repo.get_institution(query_session, "TESTBANK123")
        assert len(fi.domains) == 2

    async def test_domain_allowed(self, transaction_session: AsyncSession):
        denied_domain = DeniedDomainDao(domain="yahoo.com")
        transaction_session.add(denied_domain)
        await transaction_session.commit()
        assert await repo.is_domain_allowed(transaction_session, "yahoo.com") is False
        assert await repo.is_domain_allowed(transaction_session, "gmail.com") is True

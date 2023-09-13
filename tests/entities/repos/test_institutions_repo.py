import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from entities.models import (
    FinancialInstitutionDao,
    FinancialInstitutionDomainDao,
    FinancialInsitutionDomainCreate,
)
from entities.repos import institutions_repo as repo


class TestInstitutionsRepo:
    @pytest.fixture(scope="function", autouse=True)
    async def setup(
        self,
        session: AsyncSession,
    ):
        fi_dao_123, fi_dao_456 = FinancialInstitutionDao(
            name="Test Bank 123",
            lei="TESTBANK123",
            domains=[
                FinancialInstitutionDomainDao(domain="test.bank.1", lei="TESTBANK123")
            ],
        ), FinancialInstitutionDao(
            name="Test Bank 456",
            lei="TESTBANK456",
            domains=[
                FinancialInstitutionDomainDao(domain="test.bank.2", lei="TESTBANK456")
            ],
        )
        session.add(fi_dao_123)
        session.add(fi_dao_456)
        await session.commit()

    async def test_get_institutions(self, session: AsyncSession):
        res = await repo.get_institutions(session)
        assert len(res) == 2

    async def test_get_institutions_by_domain(self, session: AsyncSession):
        res = await repo.get_institutions(session, domain="test.bank.1")
        assert len(res) == 1

    async def test_get_institutions_by_domain_not_existing(self, session: AsyncSession):
        res = await repo.get_institutions(session, domain="testing.bank")
        assert len(res) == 0

    async def test_get_institutions_by_lei_list(self, session: AsyncSession):
        res = await repo.get_institutions(session, leis=['TESTBANK123', 'TESTBANK456'])
        assert len(res) == 2

    async def test_get_institutions_by_lei_list_item_not_existing(self, session: AsyncSession):
        res = await repo.get_institutions(session, leis=["NOTTESTBANK"])
        assert len(res) == 0

    async def test_add_institution(self, session: AsyncSession):
        await repo.upsert_institution(
            session, FinancialInstitutionDao(name="New Bank 123", lei="NEWBANK123")
        )
        res = await repo.get_institutions(session)
        assert len(res) == 3

    async def test_update_institution(self, session: AsyncSession):
        await repo.upsert_institution(
            session, FinancialInstitutionDao(name="Test Bank 234", lei="TESTBANK123")
        )
        res = await repo.get_institutions(session)
        assert len(res) == 2
        assert res[0].name == "Test Bank 234"

    async def test_add_domains(self, session: AsyncSession):
        await repo.add_domains(
            session,
            "TESTBANK123",
            [FinancialInsitutionDomainCreate(domain="bank.test")],
        )
        fi = await repo.get_institution(session, "TESTBANK123")
        assert len(fi.domains) == 2

import pytest
from sqlalchemy import text
from sqlalchemy.engine import Engine
from pytest_alembic import MigrationContext


@pytest.fixture
def alembic_config():
    return {
        "at_revision_data": {
            "7b6ff51002b5": {"__tablename__": "address_state", "code": "ZZ", "name": "TestState"},
            "26a742d97ad9": {"__tablename__": "federal_regulator", "id": "ZZZ", "name": "TestRegulator"},
            "f4ff7d1aa6df": {"__tablename__": "hmda_institution_type", "id": "00", "name": "TestHmdaInstitutionType"},
            "a41281b1e109": {"__tablename__": "sbl_institution_type", "id": "00", "name": "TestSblInstitutionType"},
        }
    }


def test_address_state_data_seed(alembic_runner: MigrationContext, alembic_engine: Engine):
    # Migrate up to, but not including this new migration
    alembic_runner.migrate_up_before("7b6ff51002b5")

    # Test address_state seed
    address_state_tablename = "address_state"
    alembic_runner.migrate_up_one()
    with alembic_engine.connect() as conn:
        address_state_rows = conn.execute(
            text("SELECT code, name from %s where code = :code" % address_state_tablename), (dict(code="AL"))
        ).fetchall()
    address_state_expected = [("AL", "Alabama")]
    assert address_state_rows == address_state_expected

    alembic_runner.migrate_down_one()
    with alembic_engine.connect() as conn:
        address_state_before_seed = conn.execute(text("SELECT code, name FROM %s" % address_state_tablename)).fetchall()
    assert address_state_before_seed == [("ZZ", "TestState")]


def test_federal_regulator_data_seed(alembic_runner: MigrationContext, alembic_engine: Engine):
    # Migrate up to, but not including this new migration
    alembic_runner.migrate_up_before("26a742d97ad9")

    # Test federal_regulator seed
    federal_regulator_tablename = "federal_regulator"
    alembic_runner.migrate_up_one()
    with alembic_engine.connect() as conn:
        federal_regulator_rows = conn.execute(
            text("SELECT id, name from %s where id = :id" % federal_regulator_tablename), (dict(id="FCA"))
        ).fetchall()
    federal_regulator_expected = [
        ("FCA", "Farm Credit Administration"),
    ]

    assert federal_regulator_rows == federal_regulator_expected

    alembic_runner.migrate_down_one()
    with alembic_engine.connect() as conn:
        federal_regulator_before_seed = conn.execute(
            text("SELECT id, name FROM %s" % federal_regulator_tablename)
        ).fetchall()
    assert federal_regulator_before_seed == [("ZZZ", "TestRegulator")]


def test_hmda_institution_type_data_seed(alembic_runner: MigrationContext, alembic_engine: Engine):
    # Migrate up to, but not including this new migration
    alembic_runner.migrate_up_before("f4ff7d1aa6df")

    # Test hmda_institution_type seed
    hmda_institution_type_tablename = "hmda_institution_type"
    alembic_runner.migrate_up_one()
    with alembic_engine.connect() as conn:
        hmda_institution_type_rows = conn.execute(
            text("SELECT id, name from %s where id = :id" % hmda_institution_type_tablename),
            (dict(id="1")),
        ).fetchall()
    hmda_institution_type_expected = [("1", "National Bank (OCC supervised)")]

    assert hmda_institution_type_rows == hmda_institution_type_expected

    alembic_runner.migrate_down_one()
    with alembic_engine.connect() as conn:
        hmda_institution_type_before_seed = conn.execute(
            text("SELECT id, name FROM %s" % hmda_institution_type_tablename)
        ).fetchall()
    assert hmda_institution_type_before_seed == [("00", "TestHmdaInstitutionType")]


def test_sbl_institution_type_data_seed(alembic_runner: MigrationContext, alembic_engine: Engine):
    # Migrate up to, but not including this new migration
    alembic_runner.migrate_up_before("a41281b1e109")

    # Test sbl_institution_type seed
    sbl_institution_type_tablename = "sbl_institution_type"
    alembic_runner.migrate_up_one()
    with alembic_engine.connect() as conn:
        sbl_institution_type_rows = conn.execute(
            text("SELECT id, name from %s where id = :id " % sbl_institution_type_tablename), (dict(id="1"))
        ).fetchall()
    sbl_institution_type_expected = [("1", "Bank or savings association")]

    assert sbl_institution_type_rows == sbl_institution_type_expected

    alembic_runner.migrate_down_one()
    with alembic_engine.connect() as conn:
        sbl_institution_type_before_seed = conn.execute(
            text("SELECT id, name FROM %s" % sbl_institution_type_tablename)
        ).fetchall()
    assert sbl_institution_type_before_seed == [("00", "TestSblInstitutionType")]


def test_denied_domains_data_seed(alembic_runner: MigrationContext, alembic_engine: Engine):
    # Migrate up to, but not including this new migration
    alembic_runner.migrate_up_before("d6e4a13fbebd")

    denied_domains_inserted = [
        ("126.com"),
        ("163.com"),
        ("21cn.com"),
        ("alice.it"),
        ("aliyun.com"),
        ("aol.com"),
        ("aol.it"),
        ("arnet.com.ar"),
        ("att.net"),
        ("bell.net"),
        ("bellsouth.net"),
        ("blueyonder.co.uk"),
        ("bol.com.br"),
        ("bt.com"),
        ("btinternet.com"),
        ("charter.net"),
        ("comcast.net"),
        ("cox.net"),
        ("daum.net"),
        ("earthlink.net"),
        ("email.com"),
        ("email.it"),
        ("facebook.com"),
        ("fastmail.fm"),
        ("fibertel.com.ar"),
        ("foxmail.com"),
        ("free.fr"),
        ("freeserve.co.uk"),
        ("games.com"),
        ("globo.com"),
        ("globomail.com"),
        ("gmail.com"),
        ("gmx.com"),
        ("gmx.de"),
        ("gmx.fr"),
        ("gmx.net"),
        ("google.com"),
        ("googlemail.com"),
        ("hanmail.net"),
        ("hotmail.be"),
        ("hotmail.ca"),
        ("hotmail.co.uk"),
        ("hotmail.com.ar"),
        ("hotmail.com.br"),
        ("hotmail.com.mx"),
        ("hotmail.com"),
        ("hotmail.de"),
        ("hotmail.es"),
        ("hotmail.fr"),
        ("hotmail.it"),
        ("hush.com"),
        ("hushmail.com"),
        ("icloud.com"),
        ("ig.com.br"),
        ("iname.com"),
        ("inbox.com"),
        ("itelefonica.com.br"),
        ("juno.com"),
        ("keemail.me"),
        ("laposte.net"),
        ("lavabit.com"),
        ("libero.it"),
        ("list.ru"),
        ("live.be"),
        ("live.co.uk"),
        ("live.com.ar"),
        ("live.com.mx"),
        ("live.com"),
        ("live.de"),
        ("live.fr"),
        ("live.it"),
        ("love.com"),
        ("mac.com"),
        ("mail.com"),
        ("mail.ru"),
        ("me.com"),
        ("msn.com"),
        ("nate.com"),
        ("naver.com"),
        ("neuf.fr"),
        ("ntlworld.com"),
        ("o2.co.uk"),
        ("oi.com.br"),
        ("online.de"),
        ("orange.fr"),
        ("orange.net"),
        ("outlook.com.br"),
        ("outlook.com"),
        ("pobox.com"),
        ("poste.it"),
        ("prodigy.net.mx"),
        ("protonmail.ch"),
        ("protonmail.com"),
        ("qq.com"),
        ("r7.com"),
        ("rambler.ru"),
        ("rocketmail.com"),
        ("rogers.com"),
        ("safe-mail.net"),
        ("sbcglobal.net"),
        ("sfr.fr"),
        ("shaw.ca"),
        ("sina.cn"),
        ("sina.com"),
        ("sky.com"),
        ("skynet.be"),
        ("speedy.com.ar"),
        ("sympatico.ca"),
        ("t-online.de"),
        ("talktalk.co.uk"),
        ("telenet.be"),
        ("teletu.it"),
        ("terra.com.br"),
        ("tin.it"),
        ("tiscali.co.uk"),
        ("tiscali.it"),
        ("tuta.io"),
        ("tutamail.com"),
        ("tutanota.com"),
        ("tutanota.de"),
        ("tvcablenet.be"),
        ("uol.com.br"),
        ("verizon.net"),
        ("virgilio.it"),
        ("virgin.net"),
        ("virginmedia.com"),
        ("voo.be"),
        ("wanadoo.co.uk"),
        ("wanadoo.fr"),
        ("web.de"),
        ("wow.com,ygm.com"),
        ("ya.ru"),
        ("yahoo.ca"),
        ("yahoo.co.id"),
        ("yahoo.co.in"),
        ("yahoo.co.jp"),
        ("yahoo.co.kr"),
        ("yahoo.co.uk"),
        ("yahoo.com.ar"),
        ("yahoo.com.br"),
        ("yahoo.com.mx"),
        ("yahoo.com.ph"),
        ("yahoo.com.sg"),
        ("yahoo.com"),
        ("yahoo.de"),
        ("yahoo.fr"),
        ("yahoo.it"),
        ("yandex.com"),
        ("yandex.ru"),
        ("yeah.net"),
        ("ymail.com"),
        ("zipmail.com.br"),
        ("zoho.com"),
    ]

    # Test denied_domains seed
    denied_domain_tablename = "denied_domains"
    alembic_runner.migrate_up_one()
    with alembic_engine.connect() as conn:
        denied_domains_rows = conn.execute(text("SELECT * FROM %s" % denied_domain_tablename)).fetchall()

    assert [elem[0] for elem in denied_domains_rows] == denied_domains_inserted

    alembic_runner.migrate_down_one()
    with alembic_engine.connect() as conn:
        denied_domains_before_seed = conn.execute(text("SELECT domain FROM %s" % denied_domain_tablename)).fetchall()
    assert denied_domains_before_seed == []

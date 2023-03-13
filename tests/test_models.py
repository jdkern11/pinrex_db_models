import os

import pytest
from sqlalchemy import create_engine
from sqlalchemy.exc import DataError
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy_utils import database_exists, create_database, drop_database

from pinrex.db import Base
from pinrex.db.models import polymer, solvent
from .test_helpers import names


@pytest.fixture(scope="session")
def connection():
    engine = create_engine(
        "postgresql+psycopg2://{}:{}@{}:{}/{}_test".format(
            os.environ.get("PINREX_DB_USER"),
            os.environ.get("PINREX_DB_PASSWORD"),
            os.environ.get("PINREX_DB_HOST"),
            os.environ.get("PINREX_DB_PORT"),
            os.environ.get("PINREX_DB_NAME"),
        )
    )
    if not database_exists(engine.url):
        create_database(engine.url)
    else:
        raise FileExistsError(
            "Database already exists. Since the database is "
            + "dropped at the end of testing, stopping the test."
        )
    yield engine.connect()

    drop_database(engine.url)


@pytest.fixture(scope="session")
def setup_database(connection):
    Base.metadata.bind = connection
    Base.metadata.create_all()

    yield

    Base.metadata.drop_all()


def seed_database(session):
    polymers = [
        {
            "pid": "P010001",
            "rid": "R1000001",
            "smiles": "[*]C[*]",
            "fingerprint": {
                "afp_H1_C4_H1": 0.3333333333333333,
                "afp_C4_C4_H1": 1.3333333333333333,
                "afp_C4_C4_C4": 0.3333333333333333,
                "bfp_197": 3.0,
                "bfp_289": 1.0,
                "bfp_304": 1.0,
                "bfp_334": 0.6666666666666666,
                "bfp_349": 0.6666666666666666,
                "bfp_359": 0.3333333333333333,
                "mfp_MQNs13": 1.0,
                "mfp_MQNs19": 0.3333333333333333,
                "mfp_MQNs29": 0.3333333333333333,
                "mfp_Chi0n": 0.8333333333333334,
                "mfp_Chi0v": 0.16666666666666666,
                "mfp_Chi1n": 0.4166666666666667,
                "mfp_Chi1v": 0.08333333333333333,
                "mfp_Chi2n": 0.041666666666666664,
                "mfp_Chi2v": 0.041666666666666664,
                "efp_numatoms_none_H": 0.3333333333333333,
                "efp_norm_mol_wt": 0.3896388888888869,
                "efp_main_chain_rel": 0.3333333333333333,
                "efp_fam_single": 1,
            },
            "category": "known",
            "canonical_smiles": "[*]C[*]",
        }
    ]
    solvents = [
        {
            "smiles": "CO",
            "fingerprint": {
                "Mafp_H1_C4_H1": 3,
                "Mafp_H1_C4_O2": 3,
                "Mafp_C4_O2_H1": 1,
                "Mbfp_267": 4.0,
                "Mbfp_311": 2.0,
                "Mbfp_349": 4.0,
                "Mbfp_359": 1.0,
                "Mmfp_MQNs13": 5.0,
                "Mmfp_MQNs19": 1.0,
                "Mmfp_MQNs20": 2.0,
                "Mmfp_MQNs21": 1.0,
                "Mmfp_MQNs27": 1.0,
                "Mmfp_MQNs29": 1.0,
                "Mmfp_Chi0n": 4.908248290463863,
                "Mmfp_Chi0v": 0.9082482904638631,
                "Mmfp_Chi1n": 2.1123724356957947,
                "Mmfp_Chi1v": 0.20412414523193154,
                "Mmfp_HallKierAlpha": 0.04,
                "Mmfp_tpsa": 5.0575,
                "Mefp_numatoms_none_H": 2,
                "Mefp_norm_mol_wt": 2.6701666666666664,
            },
            "map4_fingerprint": {"test": 3},
        }
    ]
    props = [
        {"name": "test_prop", "short_name": "tp", "unit": "t", "plot_symbol": "test"}
    ]
    for pol in polymers:
        session.add(polymer.Polymer(**pol))
    for sol in solvents:
        session.add(solvent.Solvent(**sol))
    for prop in props:
        session.add(polymer.Property(**prop))
    session.commit()


@pytest.fixture
def db_session(setup_database, connection):
    transaction = connection.begin()
    session = scoped_session(
        sessionmaker(autocommit=False, autoflush=False, bind=connection)
    )
    seed_database(session)
    yield session
    transaction.rollback()


def test_add_polymer_name(db_session, names):
    pol = (
        db_session.query(polymer.Polymer)
        .filter(polymer.Polymer.rid == "R1000001")
        .one()
    )
    for name in names.keys():
        db_session.add(
            polymer.PolymerName(pol_id=pol.id, name=name, naming_convention="unknown")
        )
    db_session.commit()

    for name, search_name in names.items():
        polymer_name = (
            db_session.query(polymer.PolymerName)
            .filter(polymer.PolymerName.name == name)
            .one()
        )
        assert polymer_name.search_name == search_name


def test_add_solvent_name(db_session, names):
    sol = db_session.query(solvent.Solvent).filter(solvent.Solvent.smiles == "CO").one()
    for name in names.keys():
        db_session.add(
            solvent.SolventName(sol_id=sol.id, name=name, naming_convention="unknown")
        )
    db_session.commit()

    for name, search_name in names.items():
        solvent_name = (
            db_session.query(solvent.SolventName)
            .filter(solvent.SolventName.name == name)
            .one()
        )
        assert solvent_name.search_name == search_name


def test_add_property_value_with_error(db_session):
    pol = db_session.query(polymer.Polymer).one()
    prop = db_session.query(polymer.Property).one()
    db_session.add(
        polymer.PolymerProperty(
            pol_id=pol.id,
            property_id=prop.id,
            value=3,
            error_value=1,
            error_type="sd",
            method="ml",
            reference="test",
            conditions={"n": 3},
        )
    )
    db_session.commit()
    prop = (
        db_session.query(polymer.PolymerProperty)
        .filter(polymer.PolymerProperty.reference == "test")
        .one()
    )
    assert prop.error_type == polymer.PolymerPropertyErrorType.sd


def test_add_property_value_with_bad_error_type(db_session):
    pol = db_session.query(polymer.Polymer).one()
    prop = db_session.query(polymer.Property).one()
    with pytest.raises(DataError):
        db_session.add(
            polymer.PolymerProperty(
                pol_id=pol.id,
                property_id=prop.id,
                value=3,
                error_value=1,
                error_type="std",
                method="ml",
                reference="test",
                conditions={"n": 3},
            )
        )
        db_session.commit()

"""Solubility/solvent related database models"""
from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    Text,
    JSON,
    UniqueConstraint,
    DateTime,
    Float,
)
from sqlalchemy.orm import relationship

from pinrex.db._base import Base
from pinrex.db.helpers import make_name_searchable


class Solvent(Base):
    """Solvents used to dissolve polymers

    Attributes:
        smiles (str):
            solvent smiles string
        fingerprint (Dict[str: float]):
            Molecular fingerprint from PolymerGenome.
        map4_fingerprint (Dict[str: int]):
            1024 dimension Fingerprint from map4
            (https://github.com/reymond-group/map4).
    """

    __tablename__ = "solvents"

    id = Column(Integer, primary_key=True, autoincrement=True)
    smiles = Column(Text, unique=True, nullable=False)
    fingerprint = Column(JSON, nullable=True)
    map4_fingerprint = Column(JSON, nullable=True)
    names = relationship("SolventName", back_populates="solvent")
    solubility_data = relationship("SolubilityData", back_populates="solvent")


class SolventName(Base):
    """Model to store the many solvent names

    Attributes:
        sol_id (int):
            Solvent the name is associated with.
        name (str):
            Name of the solvent.
        search_name (str):
            Searchable name of the solvent.
        naming_convention (str):
            How the name was created (e.g., iupac, general (not a specific solvent,
            but the general name for a grouping), unknown, abbreviation, common name).
        notes (str):
            Notes for the specific name.
    """

    __tablename__ = "solvent_names"

    id = Column(Integer, primary_key=True, autoincrement=True)
    sol_id = Column(Integer, ForeignKey("solvents.id"), nullable=False)
    name = Column(Text, nullable=False)
    search_name = Column(Text, nullable=False)
    naming_convention = Column(Text, nullable=True)
    notes = Column(Text, nullable=True)
    solvent = relationship("Solvent", back_populates="names")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.search_name = make_name_searchable(kwargs["name"])


class SolubilityData(Base):
    """Model to hold solubility data

    Attributes:
        reference (str):
            Reference where the result is taken from. Could be a literature
            reference, name of an individual, or name of a test
        date_of_test (datetime):
            Date test was performed, if available
        pol_id (int):
            Database id of polymer (not PID or RID)
        sol_id (int):
            Database id of solvent (not SID)
        solubility (str):
            Whether the solvent is a good, bad, or partial solvent for the
            polymer
        temp_min (float):
            Min temperature the solubility class is true for the pair
        temp_max (float):
            Max temperature the solubility class is true for the pair
        pol_mw_min (float):
            Smaller number of a molecular weight range for a polymer
        pol_mw_max (float):
            Larger number of a molecular weight range for a polymer
        pol_mw_type (str):
            Whether molecular weight is number or weight average
        conc_mg_per_ml (float):
            Concentration of the polymer in the solvent in mg/ml
        csst_file (int):
            id of csst file in csst_files table.
        pdi_min (float):
            Min polydispersity index.
        pdi_max (float):
            Max polydispersity index.
    """

    __tablename__ = "solubility_data"

    id = Column(Integer, primary_key=True, autoincrement=True)
    reference = Column(Text, nullable=False)
    date_added = Column(DateTime(timezone=True), nullable=False)
    pol_id = Column(Integer, ForeignKey("polymers.id"), nullable=False)
    sol_id = Column(Integer, ForeignKey("solvents.id"), nullable=False)
    solubility = Column(Text, nullable=False)
    date_of_test = Column(DateTime)
    temp_min = Column(Float)
    temp_max = Column(Float)
    pdi_min = Column(Float)
    pdi_max = Column(Float)
    pol_mw_min = Column(Float)
    pol_mw_max = Column(Float)
    pol_mw_type = Column(Text)
    conc_mg_per_ml = Column(Float)
    solvent = relationship("Solvent", back_populates="solubility_data")
    polymer = relationship("Polymer", back_populates="solubility_data")

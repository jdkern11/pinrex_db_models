from typing import Dict, List, Union
from datetime import datetime, timezone, timedelta

from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    Float,
    JSON,
    DateTime,
    Text,
    SmallInteger,
    UniqueConstraint,
)
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.dialects import postgresql

from pinrex.db_models import helpers

Base = declarative_base()


class CSSTFile(Base):
    """Model to store CSST file information

    Attributes:
        file_name (str):
            Name of crystal 16 file
        polymers (list[str]):
            List of polymers in file
        solvents (list[str]):
            List of solvents in file
        concentrations (list[float]):
            List of concentrations in file
        stir_rate (float):
            Rate of stiring referenced in file
        start_of_experiment (datetime):
            Date test was started
        version (str):
            Crystal 16 software version referenced in file
        project (str):
            Name of project referenced in file
        original_name (str):
            Original name of file from user who uploaded it
    """

    __tablename__ = "csst_files"

    id = Column(Integer, primary_key=True, autoincrement=True)
    file_name = Column(Text, unique=True, nullable=False)
    original_name = Column(Text, nullable=False)
    polymers = Column(postgresql.ARRAY(Text, dimensions=1))
    solvents = Column(postgresql.ARRAY(Text, dimensions=1))
    concentrations = Column(postgresql.ARRAY(Float, dimensions=1))
    date_added = Column(DateTime(timezone=True), nullable=False)
    stir_rate = Column(Float, nullable=False)
    start_of_experiment = Column(DateTime, nullable=False)
    version = Column(Text, nullable=False)
    project = Column(Text, nullable=False)


class Smarts(Base):
    """Smarts substructures used to search for chemical structures in smiles strings

    Attributes:
        name (str):
            Manually created name of what the smarts pattern is searching for
        smarts (str):
            Smarts pattern
        description (str):
            Description to describe the smarts pattern if needed
        reference (str):
            Where the smarts pattern was taken from
    """

    __tablename__ = "smarts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Text, nullable=True)
    smarts = Column(Text, nullable=False)
    description = Column(Text, nullable=True)
    reference = Column(Text, nullable=True)
    monomer_substructures = relationship(
        "MonomerSubstructures", back_populates="smarts"
    )


class PolymerizationReaction(Base):
    """Smarts reaction used on a smiles string to generate a polymer

    Attributes:
        name (str):
            Manually created name of what the reaction does.
        smarts (str):
            Smarts reaction.
        description (str):
            Describes the reaction if needed.
        reference (str):
            Where the smarts pattern was taken from.
    """

    __tablename__ = "polymerization_reactions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Text, nullable=True)
    smarts = Column(Text, nullable=False)
    description = Column(Text, nullable=True)
    reference = Column(Text, nullable=True)
    polymerizations = relationship(
        "Polymerization", back_populates="polymerization_reaction"
    )


class Polymerization(Base):
    """Collection of reactions that can be used on a monomer to generate a polymer

    Attributes:
        monomer_id (int):
            Monomer table id the reaction is done on.
        polymerization_reaction_id (int):
            Polymerization reaction table id the polymerization uses.
        pol_id (int):
            Polymer table id polymerization works for.

    """

    __tablename__ = "polymerizations"

    polymerization_reaction_id = Column(
        Integer,
        ForeignKey("polymerization_reactions.id"),
        nullable=False,
        primary_key=True,
    )
    monomer_id = Column(
        Integer, ForeignKey("monomers.id"), nullable=False, primary_key=True
    )
    pol_id = Column(
        Integer, ForeignKey("polymers.id"), nullable=False, primary_key=True
    )
    monomers = relationship("Monomer", back_populates="polymerizations")
    polymerization_reaction = relationship(
        "PolymerizationReaction", back_populates="polymerizations"
    )
    polymers = relationship("Polymer", back_populates="polymerizations")

    __table_args__ = (
        UniqueConstraint(
            "polymerization_reaction_id",
            "monomer_id",
            name="unique_monomer_polymerization",
        ),
    )


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
    brettmann_lab = relationship("BrettmannLab", back_populates="solvents")


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
        self.search_name = helpers.make_name_searchable(kwargs["name"])


class Polymer(Base):
    """Model to store polymer id and smiles
    Attributes:
        smiles (str):
            smiles string
        fingerprint (Dict[str, float]):
            Fingerprint dictionary
        pid (str):
            polymer id
        rid (str):
            Ramprasad group polymer id
        category (str):
            Whether the polymer is known or not
        canonical_smiles (str):
            Canonicalized version of smiles. Stored separately as some
            conformers can be removed during canonicalization (like
            cis/trans conformers).
    """

    __tablename__ = "polymers"

    id = Column(Integer, primary_key=True, autoincrement=True)
    pid = Column(Text, nullable=True)
    rid = Column(Text, unique=True, nullable=True)
    smiles = Column(Text, unique=True)
    canonical_smiles = Column(Text)
    solubility_data = relationship("SolubilityData", back_populates="polymers")
    brettmann_lab = relationship("BrettmannLab", back_populates="polymers")
    fingerprint = Column(JSON)
    category = Column(Text, nullable=True)
    properties = relationship("PolymerProperty", back_populates="polymer")
    names = relationship("PolymerName", back_populates="polymer")
    applications = relationship("PolymerApplication", back_populates="polymer")
    solubility_data = relationship("SolubilityData", back_populates="polymer")
    polymerizations = relationship("Polymerization", back_populates="polymers")


class PolymerName(Base):
    """Homopolymer names"""

    __tablename__ = "polymer_names"

    id = Column(Integer, primary_key=True, autoincrement=True)
    pol_id = Column(Integer, ForeignKey("polymers.id"), nullable=False)
    name = Column(Text, nullable=False)
    search_name = Column(Text, nullable=False)
    naming_convention = Column(Text)
    polymer = relationship("Polymer", back_populates="names")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.search_name = helpers.make_name_searchable(kwargs["name"])


class Property(Base):
    """Numerical properties for homopolymers

    Attributes:
        name (str):
            Name of the property
        short_name (str):
            Shorthand for the property (typically greek letter)
        unit (str):
            Property units
        plot_symbol (str):
            Latex string for the symbol for plotting
    """

    __tablename__ = "properties"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Text, unique=False, nullable=False)
    short_name = Column(Text, nullable=True)
    unit = Column(Text, nullable=True)
    plot_symbol = Column(Text, nullable=True)
    polymer_properties = relationship("PolymerProperty", back_populates="property")


class PolymerProperty(Base):
    """Numerical property values associated with homopolymers

    Attributes:
        pol_id (int):
            Table id of polymer in polymers table.
        property_id (int):
            Table id of property in properties table.
        value (float):
            Value of property.
        method (str):
            Method to calculate property. Could be 'exp' for experimental,
            'dft' for density functional theory, 'md' for molecular
            dynamics, or 'ml' for machine learning.
        reference (str):
            Reference property value was taken from.
    """

    __tablename__ = "polymer_properties"

    id = Column(Integer, primary_key=True, autoincrement=True)
    pol_id = Column(Integer, ForeignKey("polymers.id"), nullable=False)
    property_id = Column(Integer, ForeignKey("properties.id"), nullable=False)
    value = Column(Float, nullable=False)
    method = Column(Text, nullable=True)
    reference = Column(Text)
    note = Column(Text)
    property = relationship("Property", back_populates="polymer_properties")
    polymer = relationship("Polymer", back_populates="properties")


class PolymerApplication(Base):
    """Applications homopolymers are used to create

    Attributes:
        pol_id (int):
            Table id of polymer in polymers table.
        application (str):
            Application polymer is used in.
        category (str):
            Category of application (i.e., food packaging, automobiles, etc...)
        note (str):
            Note to further explain nuances of application (i.e., if PE is
            low density or high).
        reference (str):
            Reference application was taken from.
    """

    __tablename__ = "polymer_applications"

    id = Column(Integer, primary_key=True, autoincrement=True)
    pol_id = Column(Integer, ForeignKey("polymers.id"), nullable=False)
    application = Column(Text, nullable=False)
    category = Column(Text, nullable=False)
    note = Column(Text, nullable=True)
    reference = Column(Text, nullable=True)
    polymer = relationship("Polymer", back_populates="applications")


class Monomer(Base):
    """Possible monomers to create polymers from

    Attributes:
        smiles (str):
            smiles string
        reference_id (str):
            ID referenced from database monomer taken from
        reference (str):
            Database the reference id was taken from (ZINC15, ChEMBL)
    """

    __tablename__ = "monomers"

    id = Column(Integer, primary_key=True, autoincrement=True)
    smiles = Column(Text, unique=True, nullable=False)
    reference_id = Column(Text, nullable=True)
    reference = Column(Text, nullable=True)
    substructures = relationship("MonomerSubstructures", back_populates="monomer")
    polymerizations = relationship("Polymerization", back_populates="monomers")


class MonomerSubstructures(Base):
    """Indicates if SMARTS substructure is located in the monomer

    Attributes:
        smarts_id (int):
            Smarts id from the smarts table.
        monomer_id (int):
            Monomer id from the monomers table.
    """

    __tablename__ = "monomer_substructures"

    smarts_id = Column(
        Integer, ForeignKey("smarts.id"), nullable=False, primary_key=True
    )
    monomer_id = Column(
        Integer, ForeignKey("monomers.id"), nullable=False, primary_key=True
    )
    monomer = relationship("Monomer", back_populates="substructures")
    smarts = relationship("Smarts", back_populates="monomer_substructures")

    __table_args__ = (UniqueConstraint("smarts_id", "monomer_id", name="unique_pair"),)


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
    csst_file = Column(
        Integer, ForeignKey("csst_files.id"), unique=False, nullable=True
    )
    solvent = relationship("Solvent", back_populates="solubility_data")
    polymer = relationship("Polymer", back_populates="solubility_data")


class BrettmannLab(Base):
    """Model to store brettmann lab data

    Attributes:
        name (str):
            Name Brettmann lab refers to material as.
        pol_id (Union[None, int]):
            Polymer id. If None, material is a solvent.
        sol_id (Union[None, int]):
            Solvent id. If None, material is a polymer.
    """

    __tablename__ = "brettmann_lab"

    id = Column(Integer, primary_key=True, autoincrement=True)
    pol_id = Column(Integer, ForeignKey("polymers.id"), unique=True)
    sol_id = Column(Integer, ForeignKey("solvents.id"), unique=True)
    name = Column(Text, nullable=False, unique=True)
    solvents = relationship("Solvent", back_populates="brettmann_lab")
    polymers = relationship("Polymer", back_populates="brettmann_lab")


class ContainersAndPackagingWaste(Base):
    """Model to hold waste associated with US containers and packaging

    Attributes:
        value (int):
            Amount of waste
        year (int):
            Year waste was reported
        type (str):
            What the type of waste was (e.g., glass, plastic, steel...)
        management_pathway (str):
            What happened to the waste
        reference (str):
            Where the data was collected
        unit (str):
            Unit for value
    """

    __tablename__ = "containers_and_packaging_waste"

    id = Column(Integer, primary_key=True, autoincrement=True)
    value = Column(Integer, nullable=True)
    year = Column(SmallInteger, nullable=True)
    type = Column(Text, nullable=True)
    management_pathway = Column(Text, nullable=True)
    reference = Column(Text, nullable=True)
    unit = Column(Text, nullable=True)

"""Polymer related database models"""
from enum import unique, Enum

from sqlalchemy import Column, ForeignKey, Integer, Text, Float, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import ENUM

from pinrex.db._base import Base
from pinrex.db.helpers import make_name_searchable


@unique
class PolymerPropertyErrorType(Enum):
    """Enumerator so error types in polymer properties take specific values"""

    sd = "sd"
    sem = "sem"
    variance = "variance"


# instantiate this way so we can configure for alembic
PolymerPropertyErrorTypeEnum = ENUM(PolymerPropertyErrorType)


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
        self.search_name = make_name_searchable(kwargs["name"])


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
        error_value (float):
            Value of error type reported.
        error_type (str):
            Type of error reported. Must be one of 'sd' (standard deviation), 'sem'
            (standard error of mean), or 'variance'.
        method (str):
            Method to calculate property. Could be 'exp' for experimental,
            'dft' for density functional theory, 'md' for molecular
            dynamics, or 'ml' for machine learning.
        reference (str):
            Reference property value was taken from.
        conditions (Dict[str, Union[str, float]]):
            Conditions used to obtain the result.
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
    error_value = Column(Float)
    error_type = Column(PolymerPropertyErrorTypeEnum)
    conditions = Column(JSON)


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

"""Chemical related database models"""
from sqlalchemy import (
    Column,
    Float,
    ForeignKey,
    DateTime,
    Integer,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship

from pinrex.db._base import Base


class Chemical(Base):
    """Possible chemicals to create polymers from

    Attributes:
        smiles (str):
            smiles string
        CAS (str):
            CAS number for the chemical
    """

    __tablename__ = "chemicals"

    id = Column(Integer, primary_key=True, autoincrement=True)
    smiles = Column(Text, unique=True, nullable=False)
    cas = Column(Text)
    names = relationship("ChemicalName", back_populates="chemical")


class ChemicalSubstructures(Base):
    """Indicates if SMARTS substructure is located in the chemical

    Attributes:
        smarts_id (int):
            Smarts id from the smarts table.
        chemical_id (int):
            Chemical id from the chemicals table.
    """

    __tablename__ = "chemical_substructures"

    smarts_id = Column(
        Integer, ForeignKey("smarts.id"), nullable=False, primary_key=True
    )
    chemical_id = Column(
        Integer, ForeignKey("chemicals.id"), nullable=False, primary_key=True
    )
    chemical = relationship("Chemical", back_populates="substructures")
    smarts = relationship("Smarts", back_populates="chemical_substructures")

    __table_args__ = (UniqueConstraint("smarts_id", "chemical_id", name="chemical_smarts_pair"),)


class ChemicalSupplier(Base):
    """Vendors where the chemical can be purchased from

    Attributes:
        name (str):
            name of the vendor
        site (str):
            url of the vendor
    """

    __tablename__ = "chemical_suppliers"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Text, nullable=False)
    site = Column(Text)


class ChemicalCost(Base):
    """Cost of chemical with specific vendor at specific date

    Attributes:
        cost (float):
            cost of the chemical
        cost_unit (str):
            unit of the cost
        amount (float):
            amount recieved for the cost of the chemical
        amount_unit (str):
            unit of the amount recieved, typically gram (g) or miligram (mg)
        usd_cost_per_gram (float):
            cost per gram in U.S. dollar
        chemical_id (int):
            chemical cost references
        supplier_id (int):
            supplier the cost references
        datetime (datetime):
            date this price was found
        note (str):
            note about how the cost was collected
    """

    __tablename__ = "chemical_costs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    cost = Column(Float, nullable=False)
    cost_unit = Column(Text, nullable=False)
    amount = Column(Float, nullable=False)
    amount_unit = Column(Text, nullable=False)
    usd_cost_per_gram = Column(Float, nullable=False)
    chemical_id = Column(Integer, ForeignKey("chemicals.id"), nullable=False)
    supplier_id = Column(Integer, ForeignKey("chemical_suppliers.id"), nullable=False)
    datetime = Column(DateTime, nullable=False)
    note = Column(Text)


def ChemicalName(Base):
    """

    Attributes:
        name (str): Name of the chemical
        search_name (str): Method to search name, see
            pinrex.db.helpers.make_name_searchable
        chemical_id (int): chemical id the name references
    """
    __tablename__ = "chemical_names"

    id = Column(Integer, primary_key=True, autoincrement=True)
    chemical_id = Column(Integer, ForeignKey("chemicals.id"), nullable=False)
    name = Column(Text, nullable=False)
    search_name = Column(Text, nullable=False)
    naming_convention = Column(Text)
    notes = Column(Text, nullable=True)
    chemical = relationship("Chemical", back_populates="names")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.search_name = make_name_searchable(kwargs["name"])

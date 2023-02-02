"""Monomer related database models"""
from sqlalchemy import Column, ForeignKey, Integer, Text, UniqueConstraint
from sqlalchemy.orm import relationship

from pinrex.db._base import Base


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

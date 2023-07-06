"""molecular structure related database models"""
from sqlalchemy import Column, Integer, Text
from sqlalchemy.orm import relationship

from pinrex.db._base import Base


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
    chemical_substructures = relationship(
        "ChemicalSubstructure", back_populates="smarts"
    )

    reaction_procedures = relationship(
        "ReactionProcedureStartingSubstructure", back_populates="smarts"
    )

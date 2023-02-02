"""Virtual lab database models"""
from sqlalchemy import Column, ForeignKey, Integer, Text
from sqlalchemy.orm import relationship

from pinrex.db._base import Base


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

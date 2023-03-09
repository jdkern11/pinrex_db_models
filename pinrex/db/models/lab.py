"""Virtual lab database models"""
from sqlalchemy import Column, ForeignKey, Integer, Text
from sqlalchemy.orm import relationship

from pinrex.db._base import Base


class BrettmannLabPolymer(Base):
    """Model to store brettmann lab data

    Attributes:
        pol_id (int):
            Polymer id. If None, material is a solvent.
        name (str):
            Name the brettmann lab refers to the polymer as.
    """

    __tablename__ = "brettmann_lab_polymers"

    id = Column(Integer, primary_key=True, autoincrement=True)
    pol_id = Column(Integer, ForeignKey("polymers.id"))
    name = Column(Text, nullable=False, unique=True)


class BrettmannLabSolvent(Base):
    """Model to store brettmann lab data

    Attributes:
        sol_id (Union[None, int]):
            Polymer id. If None, material is a solvent.
        name (str):
            Name the brettmann lab refers to the solvent as.
    """

    __tablename__ = "brettmann_lab_solvents"

    id = Column(Integer, primary_key=True, autoincrement=True)
    sol_id = Column(Integer, ForeignKey("solvents.id"))
    name = Column(Text, nullable=True)

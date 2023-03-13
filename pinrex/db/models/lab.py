"""Virtual lab database models"""
from sqlalchemy import Column, ForeignKey, Integer, Text, Float
from sqlalchemy.orm import relationship

from pinrex.db._base import Base


class BrettmannLabPolymer(Base):
    """Model to store brettmann lab data

    Attributes:
        pol_id (int):
            Polymer id. If None, material is a solvent.
        name (str):
            Name the brettmann lab refers to the polymer as.
        number_average_mw_min (float):
            Min number average molecular weight assosicated with the sample
        number_average_mw_max (float):
            Max number average molecular weight assosicated with the sample
        supplier (str):
            Supplier of the sample
    """

    __tablename__ = "brettmann_lab_polymers"

    id = Column(Integer, primary_key=True, autoincrement=True)
    pol_id = Column(Integer, ForeignKey("polymers.id"))
    name = Column(Text, nullable=False, unique=False)
    number_average_mw_min = Column(Float, nullable=True)
    number_average_mw_max = Column(Float, nullable=True)
    supplier = Column(Text, nullable=True)

class BrettmannLabSolvent(Base):
    """Model to store brettmann lab data

    Attributes:
        sol_id (Union[None, int]):
            Polymer id. If None, material is a solvent.
        name (str):
            Name the brettmann lab refers to the solvent as.
        percent_purity (float):
            Percent purity of the solvent
    """

    __tablename__ = "brettmann_lab_solvents"

    id = Column(Integer, primary_key=True, autoincrement=True)
    sol_id = Column(Integer, ForeignKey("solvents.id"))
    name = Column(Text, nullable=True, unique=False)
    percent_purity = Column(Float, nullable=True)

"""Miscellaneous data models (e.g., plastic waste data)"""
from sqlalchemy import Column, Integer, Text, SmallInteger

from pinrex.db._base import Base


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

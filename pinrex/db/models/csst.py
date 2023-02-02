"""Crystal 16 database models"""
from sqlalchemy import Column, Integer, Float, DateTime, Text
from sqlalchemy.dialects.postgresql import ARRAY

from pinrex.db._base import Base


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
    polymers = Column(ARRAY(Text, dimensions=1))
    solvents = Column(ARRAY(Text, dimensions=1))
    concentrations = Column(ARRAY(Float, dimensions=1))
    date_added = Column(DateTime(timezone=True), nullable=False)
    stir_rate = Column(Float, nullable=False)
    start_of_experiment = Column(DateTime, nullable=False)
    version = Column(Text, nullable=False)
    project = Column(Text, nullable=False)

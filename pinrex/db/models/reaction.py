"""Polymerization related database models"""
from sqlalchemy import Column, ForeignKey, Integer, Text, UniqueConstraint
from sqlalchemy.orm import relationship

from pinrex.db._base import Base

class Reaction(Base):
    """Individual reaction

    Attributes:
        smarts (str):
            Smarts reaction.
        description (str):
            Describes the reaction if needed.
        reference (str):
            Where the smarts pattern was taken from.
    """

    __tablename__ = "reactions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    smarts = Column(Text, nullable=False)
    description = Column(Text, nullable=True)
    reference = Column(Text, nullable=True)

class ReactionStep(Base):
    """Links reaction to specific step in reaction procedure

    Attributes:
        reaction_id (int):
            Id in reaction.Reaction table
        reaction_procedure_id (int):
            Id in reaction.ReactionProcedure table
        step (int):
            Step in the process (indexing starts at 1)
    """

    __tablename__ = "reaction_steps"

class ReactionProcedure(Base):
    """Polymer reaction that consists of several steps

    Attributes:
        description (str):
            Name of the reaction that is occuring
    """

    __tablename__ = "reaction_procedures"

class ReactionPolymerMapping(Base):
    """Maps reaction procedure, starting chemical, and polymer

    Attributes:
        reaction_procedure_id (int): 
            Id in reaction.ReactionProcedure table
        pol_id (int): 
            Id in polymer.Polymer table
        chemical_id (int): 
            Id in chemical.Chemical table
    """

    __tablename__ = "reaction_polymer_mappings"

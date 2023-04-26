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

    steps = relationship("ReactionStep", back_populates="reactions")


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

    reaction_id = Column(
        Integer,
        ForeignKey("reactions.id"),
        nullable=False,
        primary_key=True,
    )
    reaction_procedure_id = Column(
        Integer,
        ForeignKey("reaction_procedures.id"),
        nullable=False,
        primary_key=True,
    )
    step = Column(Integer, nullable=False, primary_key=True)

    reactions = relationship("Reaction", back_populates="steps")
    procedures = relationship("ReactionProcedure", back_populates="steps")

    __table_args__ = (
        UniqueConstraint(
            "reaction_procedure_id",
            "reaction_id",
            "step",
            name="unique_reaction_step",
        ),
    )


class ReactionProcedure(Base):
    """Polymer reaction that consists of several steps

    Attributes:
        name (str):
            Name of the reaction procedure
        description (str):
            Name of the reaction that is occuring
    """

    __tablename__ = "reaction_procedures"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Text, nullable=False, unique=True)
    description = Column(Text, nullable=True)

    steps = relationship("ReactionStep", back_populates="procedures")
    mappings = relationship("ReactionPolymerMapping", back_populates="procedures")
    smarts = relationship(
        "ReactionProcedureStartingSubstructure", back_populates="procedures"
    )


class ReactionProcedureStartingSubstructure(Base):
    """Starting substructure needed for reaction procedure

    Attributes:
        reaction_procedure_id (int): ReactionProcedure table id
        smarts_id (int): structure.Smarts table id
    """

    __tablename__ = "reaction_procedure_starting_substructure"

    reaction_procedure_id = Column(
        Integer,
        ForeignKey("reaction_procedures.id"),
        nullable=False,
        primary_key=True,
    )

    smarts_id = Column(
        Integer, ForeignKey("smarts.id"), nullable=False, primary_key=True
    )

    smarts = relationship("Smarts", back_populates="reaction_procedures")
    procedures = relationship("ReactionProcedure", back_populates="smarts")

    __table_args__ = (
        UniqueConstraint(
            "reaction_procedure_id",
            "smarts_id",
            name="unique_reaction_procedure_starting_substructure",
        ),
    )


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

    reaction_procedure_id = Column(
        Integer,
        ForeignKey("reaction_procedures.id"),
        nullable=False,
        primary_key=True,
    )
    chemical_id = Column(
        Integer, ForeignKey("chemicals.id"), nullable=False, primary_key=True
    )
    pol_id = Column(
        Integer, ForeignKey("polymers.id"), nullable=False, primary_key=True
    )

    procedures = relationship("ReactionProcedure", back_populates="mappings")
    polymer = relationship("Polymer", back_populates="reaction_mappings")
    chemical = relationship("Chemical", back_populates="reaction_mappings")

    __table_args__ = (
        UniqueConstraint(
            "reaction_procedure_id",
            "pol_id",
            "chemical_id",
            name="unique_reaction_polymer_mapping",
        ),
    )

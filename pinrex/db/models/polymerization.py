"""Polymerization related database models"""
from sqlalchemy import Column, ForeignKey, Integer, Text, UniqueConstraint
from sqlalchemy.orm import relationship

from pinrex.db._base import Base


class PolymerizationReaction(Base):
    """Smarts reaction used on a smiles string to generate a polymer

    Attributes:
        name (str):
            Manually created name of what the reaction does.
        smarts (str):
            Smarts reaction.
        description (str):
            Describes the reaction if needed.
        reference (str):
            Where the smarts pattern was taken from.
    """

    __tablename__ = "polymerization_reactions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Text, nullable=True)
    smarts = Column(Text, nullable=False)
    description = Column(Text, nullable=True)
    reference = Column(Text, nullable=True)
    polymerizations = relationship(
        "Polymerization", back_populates="polymerization_reaction"
    )


class Polymerization(Base):
    """Collection of reactions that can be used on a monomer to generate a polymer

    Attributes:
        monomer_id (int):
            Monomer table id the reaction is done on.
        polymerization_reaction_id (int):
            Polymerization reaction table id the polymerization uses.
        pol_id (int):
            Polymer table id polymerization works for.

    """

    __tablename__ = "polymerizations"

    polymerization_reaction_id = Column(
        Integer,
        ForeignKey("polymerization_reactions.id"),
        nullable=False,
        primary_key=True,
    )
    monomer_id = Column(
        Integer, ForeignKey("monomers.id"), nullable=False, primary_key=True
    )
    pol_id = Column(
        Integer, ForeignKey("polymers.id"), nullable=False, primary_key=True
    )
    monomers = relationship("Monomer", back_populates="polymerizations")
    polymerization_reaction = relationship(
        "PolymerizationReaction", back_populates="polymerizations"
    )
    polymers = relationship("Polymer", back_populates="polymerizations")

    __table_args__ = (
        UniqueConstraint(
            "polymerization_reaction_id",
            "monomer_id",
            name="unique_monomer_polymerization",
        ),
    )

"""All db models for data related to toxicity"""
from enum import unique, Enum

from sqlalchemy import Column, ForeignKey, Integer, Text, Float, JSON
from sqlalchemy.dialects.postgresql import ARRAY, ENUM

from pinrex.db._base import Base


@unique
class TargetModeOfAction(Enum):
    """Enumerator for assay target modes of action"""

    agonist = "agonist"
    antagonist = "antagonist"
    permeabilization = "permeabilization"
    inhibition = "inhibition"
    activation = "activation"


@unique
class Activity(Enum):
    """Enumerator for activity of molecule in an assay"""

    active = "active"
    inactive = "inactive"
    inconclusive = "inconclusive"


# instantiate this way so we can configure for alembic
TargetModeOfActionEnum = ENUM(TargetModeOfAction)
ActivityEnum = ENUM(Activity)


class Gene(Base):
    """Model to store gene information

    Attributes:
        name:
            Name of the gene
        uniprot_id:
            uniprot id. UniProt is a database of protein sequence and functional
            information.
    """

    __tablename__ = "genes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Text, unique=True, nullable=False)
    uniprot_id = Column(Integer, unique=True)


class ExperimentalCellLine(Base):
    """Model to store cell line information for assays

    Attributes:
        name (str):
            Name of the cell line.
        cell (str):
            Cell the cell line is modified from.
        cell_clo_id (str):
            Cell line ontology id experimental cell line was derived from.
        experimental_cell_clo_id (str):
            Cell line ontology id of the experimental cell line.
        cellosaurus_id (str):
            Cellosaurus is a knowledge resource on cell lines. This is the id in
            cellosaurs for the cell line the experimental cell line is modified from.
        organism (str):
            Species of origin.
        organism_taxon_id (int):
            Taxon id of the species of origin.
    """

    __tablename__ = "experimental_cell_lines"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Text, unique=True, nullable=False)
    experimental_cell_clo_id = Column(Text, unique=True, nullable=False)
    cell = Column(Text)
    cell_clo_id = Column(Text)
    cellosaurus_id = Column(Text)
    organism = Column(Text)
    organism_taxon_id = Column(Integer)


class ToxAssay(Base):
    """Model to store toxicity assay data

    Attributes:
        assay_type (str):
            If the assay is a reporter assay or counter screen (toxicity assay).
        pair_id (int):
            Reporters are paired with counter screens. This id represents which
            ids are paired together in the database.
        pubchem_aid (int):
            pubchem assay id.
        tox21_aid (str):
            tox21 assay id.
        reporter_gene_assay (str):
            what reporter is used in the assay if it is a reporter assay.
        exp_cell_line_id (int):
            ID of the experimental cell line used in the assay.
        gene_id (int):
            ID of the gene tested.
        target (str):
            Biological pathways or molecules that a compound is intended to interact with.
        target_effect (str):
            Effect of the compound on the target.
        target_mode_of_action (str):
            If the compound is antagonistic, agonistic, causing permeabilization, or
            causing inhibition.
        kit (str):
            Kit used in the assay.
        physical_detection_method (str):
            Method to assess activity in the assay.
        detection_instrument (str):
            Instrument used to detect the physical detection method.
        definition (str):
            What the assay is testing for
    """

    __tablename__ = "tox_assays"

    id = Column(Integer, primary_key=True, autoincrement=True)
    assay_type = Column(Text, nullable=False)
    pair_id = Column(Integer)
    pubchem_aid = Column(Integer)
    tox21_aid = Column(Integer)
    reporter_gene_assay = Column(Text)
    exp_cell_line_id = Column(
        Integer, ForeignKey("experimental_cell_lines.id"), nullable=False
    )
    gene_id = Column(Integer, ForeignKey("genes.id"))
    target = Column(Text, nullable=False)
    target_effect = Column(Text, nullable=False)
    target_mode_of_action = Column(TargetModeOfActionEnum, nullable=False)
    kit = Column(Text)
    physical_detection_method = Column(Text)
    detection_instrument = Column(Text)
    definition = Column(Text)


class Tox21Molecule(Base):
    """Model to store molecule data from the tox21 dataset

    Attribute:
        pubchem_cid (int):
            ID of the compound in pubchem
        tox21_sid (List[int]):
            Tox21 substance id. Compounds can have multiple substance ids
        smiles (str):
            Smiles of the molecules
        fingerprint (Dict[str, float]):
            Polymer genome molecule fingerprint for the compound
        cluster (int):
            Cluster the compound belongs to based on the paper
            Cooper and Schürer, “Improving the Utility of the Tox21 Dataset by
            Deep Metadata Annotations and Constructing Reusable Benchmarked Chemical
            Reference Signatures,” Molecules, vol. 24, no. 8, p. 1604, Apr. 2019,
            doi: 10.3390/molecules24081604.
    """

    __tablename__ = "tox21_molecules"

    id = Column(Integer, primary_key=True, autoincrement=True)
    pubchem_aid = Column(Integer)
    tox21_sid = Column(ARRAY(Integer, dimensions=1))
    smiles = Column(Text, nullable=False)
    fingerprint = Column(JSON)
    cluser = Column(Integer)


class Tox21Data(Base):
    """Model to store tox21 data

    Attribute:
        molecule_id (int):
            Tox21Molecule id
        assay_id (int):
            ToxAssay id
        activity (str):
            activity of molecule, either active, inactive, or inconclusive
        pac50_val (float):
            AC50 value of the molecule. I am unsure what the units are.
        reference (str):
            Where the data was collected from.
    """

    __tablename__ = "tox21_data"

    id = Column(Integer, primary_key=True, autoincrement=True)
    molecule_id = Column(Integer, ForeignKey("tox21_molecules.id"), nullable=False)
    assay_id = Column(Integer, ForeignKey("tox_assays.id"), nullable=False)
    activity = Column(ActivityEnum, nullable=False)
    pac50_val = Column(Float)
    reference = Column(Text)

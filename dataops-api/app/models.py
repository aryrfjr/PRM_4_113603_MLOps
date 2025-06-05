from datetime import datetime
from sqlalchemy import (
    String,
    Text,
    DateTime,
    ForeignKey,
    UniqueConstraint,
    Index,
)
from sqlalchemy.orm import relationship, Mapped, mapped_column
from .database import Base

########################################################################
#
# SQLAlchemy Object-Relational Mapping (ORM) models:
#
# - Fully typed with SQLAlchemy 2.0.
# - Referential integrity via foreign keys.
# - Auto-cascade deletes where appropriate.
# - Indexes on lookup fields (bond_type, run_id, status).
# - Bidirectional relationships enable easy ORM navigation.
#
########################################################################


#
# Nominal Composition
#
########################################################################
class NominalComposition(Base):
    __tablename__ = "nominal_compositions"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    runs = relationship(
        "Run", back_populates="nominal_composition", cascade="all, delete-orphan"
    )


#
# Run
#
########################################################################
class Run(Base):
    __tablename__ = "runs"
    __table_args__ = (
        UniqueConstraint("nominal_composition_id", "run_number", name="unique_run"),
        Index("idx_runs_nominal_composition", "nominal_composition_id"),
        Index("idx_runs_status", "status"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    nominal_composition_id: Mapped[int] = mapped_column(
        ForeignKey("nominal_compositions.id", ondelete="CASCADE"), nullable=False
    )
    run_number: Mapped[int] = mapped_column(nullable=False)
    status: Mapped[str] = mapped_column(String(20), default="SCHEDULED")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    nominal_composition = relationship("NominalComposition", back_populates="runs")
    sub_runs = relationship(
        "SubRun", back_populates="run", cascade="all, delete-orphan"
    )


#
# SubRun
#
########################################################################
class SubRun(Base):
    __tablename__ = "sub_runs"
    __table_args__ = (
        UniqueConstraint("run_id", "sub_run_number", name="unique_sub_run"),
        Index("idx_sub_runs_run_id", "run_id"),
        Index("idx_sub_runs_status", "status"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    run_id: Mapped[int] = mapped_column(
        ForeignKey("runs.id", ondelete="CASCADE"), nullable=False
    )
    sub_run_number: Mapped[int] = mapped_column(nullable=False)
    status: Mapped[str] = mapped_column(String(20), default="SCHEDULED")
    scheduled_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    completed_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)

    run = relationship("Run", back_populates="sub_runs")
    descriptor_files = relationship(
        "DescriptorFile", back_populates="sub_run", cascade="all, delete-orphan"
    )
    simulation_artifacts = relationship(
        "SimulationArtifact", back_populates="sub_run", cascade="all, delete-orphan"
    )
    bonds = relationship(
        "BondInteraction", back_populates="sub_run", cascade="all, delete-orphan"
    )


#
# Descriptor Files
#
########################################################################
class DescriptorFile(Base):
    __tablename__ = "descriptor_files"
    __table_args__ = (
        UniqueConstraint("sub_run_id", "bond_type", name="unique_descriptor_per_bond"),
        Index("idx_descriptor_sub_run", "sub_run_id"),
        Index("idx_descriptor_bond_type", "bond_type"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    sub_run_id: Mapped[int] = mapped_column(
        ForeignKey("sub_runs.id", ondelete="CASCADE"), nullable=False
    )
    bond_type: Mapped[str] = mapped_column(String(20), nullable=False)
    file_path: Mapped[str] = mapped_column(Text, nullable=False)
    file_size: Mapped[int] = mapped_column(nullable=True)
    checksum: Mapped[str] = mapped_column(String(64), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    sub_run = relationship("SubRun", back_populates="descriptor_files")
    bonds = relationship("BondInteraction", back_populates="descriptor_file")


#
# Simulation Artifacts
#
########################################################################
class SimulationArtifact(Base):
    __tablename__ = "simulation_artifacts"
    __table_args__ = (
        UniqueConstraint(
            "sub_run_id", "artifact_type", name="unique_artifact_per_type"
        ),
        Index("idx_artifact_sub_run", "sub_run_id"),
        Index("idx_artifact_type", "artifact_type"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    sub_run_id: Mapped[int] = mapped_column(
        ForeignKey("sub_runs.id", ondelete="CASCADE"), nullable=False
    )
    artifact_type: Mapped[str] = mapped_column(
        String(50), nullable=False
    )  # e.g., 'QE_scf_in'
    file_path: Mapped[str] = mapped_column(Text, nullable=False)
    file_size: Mapped[int] = mapped_column(nullable=True)
    checksum: Mapped[str] = mapped_column(String(64), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    sub_run = relationship("SubRun", back_populates="simulation_artifacts")


#
# Bond Interactions (DBI)
#
########################################################################
class BondInteraction(Base):
    __tablename__ = "bonds_interactions"
    __table_args__ = (
        UniqueConstraint(
            "sub_run_id", "atom_a_idx", "atom_b_idx", name="unique_bond_pair"
        ),
        Index("idx_bonds_sub_run", "sub_run_id"),
        Index("idx_bonds_atom_pair", "atom_a_element", "atom_b_element"),
        Index("idx_bonds_distance", "bond_distance"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    sub_run_id: Mapped[int] = mapped_column(
        ForeignKey("sub_runs.id", ondelete="CASCADE"), nullable=False
    )
    atom_a_idx: Mapped[int] = mapped_column(nullable=False)
    atom_b_idx: Mapped[int] = mapped_column(nullable=False)
    atom_a_element: Mapped[str] = mapped_column(String(5), nullable=False)
    atom_b_element: Mapped[str] = mapped_column(String(5), nullable=False)
    bond_distance: Mapped[float] = mapped_column(nullable=False)
    bond_icohp: Mapped[float] = mapped_column(nullable=True)

    descriptor_file_id: Mapped[int] = mapped_column(
        ForeignKey("descriptor_files.id", ondelete="SET NULL"), nullable=True
    )

    sub_run = relationship("SubRun", back_populates="bonds")
    descriptor_file = relationship("DescriptorFile", back_populates="bonds")


#
# Mixed Databases (DBI Mixes)
#
########################################################################
class MixedDatabase(Base):
    __tablename__ = "mixed_databases"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    entries = relationship(
        "MixedDatabaseEntry", back_populates="mixed_db", cascade="all, delete-orphan"
    )


class MixedDatabaseEntry(Base):
    __tablename__ = "mixed_database_entries"
    __table_args__ = (
        Index("idx_mixed_entries_db_id", "mixed_db_id"),
        Index("idx_mixed_entries_bond_type", "bond_type"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    mixed_db_id: Mapped[int] = mapped_column(
        ForeignKey("mixed_databases.id", ondelete="CASCADE"), nullable=False
    )
    descriptor_file_id: Mapped[int] = mapped_column(
        ForeignKey("descriptor_files.id", ondelete="CASCADE"), nullable=False
    )
    bond_type: Mapped[str] = mapped_column(String(20), nullable=False)

    mixed_db = relationship("MixedDatabase", back_populates="entries")
    descriptor_file = relationship("DescriptorFile")

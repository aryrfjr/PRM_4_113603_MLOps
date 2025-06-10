from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum

########################################################################
#
# Pydantic schemas for request/response
#
########################################################################


#
# General jobs and data generation status flags
#
##########################################################################


class Status(Enum):
    SCHEDULED = "SCHEDULED"
    DONE = "DONE"
    RUNNING = "RUNNING"
    FAILED = "FAILED"


#
# Possible values for 'artifact_type' field in the DB table 'simulation_artifacts'
#
##########################################################################


class ArtifactType(str, Enum):
    # LAMMPS
    LAMMPS_DUMP = "LAMMPS_dump"  # only SubRun 0
    LAMMPS_LOG = "LAMMPS_log"  # only SubRun 0
    LAMMPS_INPUT = "LAMMPS_input"  # only SubRun 0
    LAMMPS_OUTPUT = "LAMMPS_output"  # only SubRun 0
    LAMMPS_DUMP_XYZ = "LAMMPS_dump_xyz"  # only SubRun 0

    # QE
    QE_SCF_IN = "QE_scf_in"  # all SubRuns
    QE_SCF_OUT = "QE_scf_out"  # all SubRuns

    # LOBSTER
    LOBSTER_INPUT = "LOBSTER_input"  # all SubRuns
    LOBSTER_INPUT_BND = "LOBSTER_input_bnd"  # all SubRuns
    LOBSTER_OUTPUT = "LOBSTER_output"  # all SubRuns
    LOBSTER_RUN_OUTPUT = "LOBSTER_run_output"  # all SubRuns
    ICOHPLIST = "ICOHPLIST"  # all SubRuns

    # SOAP (optional)
    SOAP_VECTORS = "SOAP_vectors"  # all SubRuns


class SimulationArtifactInfo(BaseModel):
    artifact_type: ArtifactType
    file_path: str
    file_size: Optional[int]
    checksum: Optional[str]
    created_at: datetime


#
# CRUD for DB table nominal_compositions
#
########################################################################


class NominalCompositionBase(BaseModel):
    name: str = Field(..., example="Zr49Cu49Al2")
    description: Optional[str] = Field(None, example="A typical metallic glass")


class NominalCompositionCreate(NominalCompositionBase):
    pass


class NominalCompositionUpdate(BaseModel):
    name: Optional[str] = Field(None, example="Zr50Cu50")  # Allow rename
    description: Optional[str] = Field(None, example="Updated description")

    class Config:  # NOTE: Inner class for configuration of the Pydantic model
        orm_mode = (
            True  # NOTE: can be created from Object-Relational Mapping (ORM) objects
        )
        from_attributes = True


class NominalCompositionResponse(NominalCompositionBase):
    id: int
    created_at: datetime

    class Config:  # NOTE: Inner class for configuration of the Pydantic model
        orm_mode = (
            True  # NOTE: can be created from Object-Relational Mapping (ORM) objects
        )
        from_attributes = True


#
# Data Generation & Labeling (DataOps) phase
#
########################################################################


class ExploitationJobResponse(BaseModel):
    id: int
    sub_run_number: int
    status: str
    scheduled_at: datetime
    completed_at: Optional[datetime]

    class Config:  # NOTE: Inner class for configuration of the Pydantic model
        orm_mode = (
            True  # NOTE: can be created from Object-Relational Mapping (ORM) objects
        )
        from_attributes = True


class ExplorationJobBaseResponse(BaseModel):
    id: int
    run_number: int
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:  # NOTE: Inner class for configuration of the Pydantic model
        orm_mode = (
            True  # NOTE: can be created from Object-Relational Mapping (ORM) objects
        )
        from_attributes = True


class ExplorationJobFullResponse(ExplorationJobBaseResponse):
    sub_runs: List[ExploitationJobResponse] = []


class ScheduleExplorationRequest(BaseModel):
    num_simulations: int = Field(..., gt=0, example=3)


class RunWithSubRunIds(BaseModel):
    id: int
    run_number: int
    sub_runs: List[int]


class ScheduleExploitationRequest(BaseModel):
    runs: List[RunWithSubRunIds]


class GenericStatusResponse(BaseModel):
    message: str
    status: Status


# NOTE: The ETL model is a two step process originally implemented with the
# scripts 'create_SSDB.py' (for a single NC) and 'mix_SSDBs.py' (for multiple NCs).
#
# TODO: update the request payload to meet that reality.
class ETLModelRequest(BaseModel):
    nominal_composition: str = Field(..., example="Zr49Cu49Al2")


class ETLModelResponse(GenericStatusResponse):
    pass


#
# Model Development (ModelOps) phase
#
########################################################################


class EvaluateModelRequest(BaseModel):
    model_name: str = Field(..., example="GPR_SOAP_Bonds_v1")
    test_set: str = Field(..., example="DB8_Test")


class EvaluateModelResponse(GenericStatusResponse):
    pass


#
# Miscellaneous
#
########################################################################


class PingResponse(BaseModel):
    message: str

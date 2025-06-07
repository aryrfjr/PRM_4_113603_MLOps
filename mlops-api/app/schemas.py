from pydantic import BaseModel, Field
from typing import Optional, Literal
from datetime import datetime
from enum import Enum

########################################################################
#
# Pydantic models for request/response
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


class GenericStatusResponse(BaseModel):
    message: str
    status: Literal[Status.SCHEDULED, Status.FAILED, Status.DONE, Status.RUNNING]


# NOTE: The ETL model is a two step process originally implemented with the
# scripts 'create_SSDB.py' (for a single NC) and 'mix_SSDBs.py' (for multiple NCs).
#
# TODO: update the request payload for that reality.
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

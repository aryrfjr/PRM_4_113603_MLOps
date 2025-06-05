from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

########################################################################
#
# Pydantic models for request/response
#
########################################################################

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
# Miscellaneous
#
########################################################################


class PingResponse(BaseModel):
    message: str

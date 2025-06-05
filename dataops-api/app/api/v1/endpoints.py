from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app import models, schemas

from datetime import datetime

##########################################################################
#
# Globals
#
##########################################################################

router = APIRouter()

#
# General descriptions and examples for Swagger documentation
#
##########################################################################

#
# General jobs and data generation status flags
#
##########################################################################

##########################################################################
#
# Subroutines
#
##########################################################################

##########################################################################
#
# Endpoints for different resources types and scopes.
#
# TODO: review status codes.
#
# TODO: review error handling: consistent and descriptive error responses,
#  with machine-readable codes and human-readable messages.
#
# TODO: Authentication (API key or OAuth2 support).
#
# TODO: Event-driven trigger (API could emit events, like job completed,
#  to Airflow or MLflow to trigger downstream tasks.
#
##########################################################################


#
# CRUD for DB table nominal_compositions
#
########################################################################


# Create Nominal Composition
@router.post(
    "/nominal_compositions/",
    response_model=schemas.NominalCompositionResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_nominal_composition(
    payload: schemas.NominalCompositionCreate, db: Session = Depends(get_db)
):
    existing = db.query(models.NominalComposition).filter_by(name=payload.name).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Nominal composition '{payload.name}' already exists.",
        )

    nc = models.NominalComposition(
        name=payload.name, description=payload.description, created_at=datetime.utcnow()
    )
    db.add(nc)
    db.commit()
    db.refresh(nc)

    return schemas.NominalCompositionResponse.from_orm(nc)


# Get Nominal Composition by Name
@router.get(
    "/nominal_compositions/{name}", response_model=schemas.NominalCompositionResponse
)
def get_nominal_composition(name: str, db: Session = Depends(get_db)):
    nc = db.query(models.NominalComposition).filter_by(name=name).first()
    if not nc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Nominal composition '{name}' not found.",
        )
    return schemas.NominalCompositionResponse.from_orm(nc)


# List All Nominal Compositions
@router.get(
    "/nominal_compositions/", response_model=List[schemas.NominalCompositionResponse]
)
def list_nominal_compositions(db: Session = Depends(get_db)):
    ncs = (
        db.query(models.NominalComposition)
        .order_by(models.NominalComposition.name)
        .all()
    )
    return [schemas.NominalCompositionResponse.from_orm(nc) for nc in ncs]


# Update Nominal Composition
@router.put(
    "/nominal_compositions/{name}", response_model=schemas.NominalCompositionResponse
)
def update_nominal_composition(
    name: str, payload: schemas.NominalCompositionUpdate, db: Session = Depends(get_db)
):
    nc = db.query(models.NominalComposition).filter_by(name=name).first()

    if not nc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Nominal composition '{name}' not found.",
        )

    if payload.name:
        nc.name = payload.name
    if payload.description is not None:
        nc.description = payload.description

    db.commit()
    db.refresh(nc)

    return schemas.NominalCompositionResponse.from_orm(nc)


# Delete Nominal Composition
@router.delete("/nominal_compositions/{name}", status_code=status.HTTP_204_NO_CONTENT)
def delete_nominal_composition(name: str, db: Session = Depends(get_db)):
    nc = db.query(models.NominalComposition).filter_by(name=name).first()

    if not nc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Nominal composition '{name}' not found.",
        )

    db.delete(nc)
    db.commit()

    return None


#
# Miscellaneous
#
########################################################################
@router.get("/ping", response_model=schemas.PingResponse)
def ping():
    return {"message": "PING OK"}

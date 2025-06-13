from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timezone

from app.database import get_db
from app import models, schemas

##########################################################################
#
# Globals
#
##########################################################################

router = APIRouter()

##########################################################################
#
# Helpers
#
##########################################################################

#
# CRUD for DB table nominal_compositions
#
########################################################################


# Creates a Nominal Composition entry
@router.post(
    "/nominal_compositions/",
    response_model=schemas.NominalCompositionResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["CRUD"],
    summary="Creates a Nominal Composition entry.",
    description="Creates a Nominal Composition entry.",
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
        name=payload.name,
        description=payload.description,
        created_at=datetime.now(timezone.utc),
    )

    db.add(nc)
    db.commit()
    db.refresh(nc)

    return schemas.NominalCompositionResponse.from_orm(nc)


# Retrieves a NominalComposition by name
@router.get(
    "/nominal_compositions/{name}",
    response_model=schemas.NominalCompositionResponse,
    tags=["CRUD"],
    summary="Retrieves a NominalComposition by name.",
    description="Retrieves a NominalComposition by name.",
)
def get_nominal_composition(name: str, db: Session = Depends(get_db)):

    nc = db.query(models.NominalComposition).filter_by(name=name).first()

    if not nc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Nominal composition '{name}' not found.",
        )

    return schemas.NominalCompositionResponse.from_orm(nc)


# Lists all NominalCompositions ordered by name
@router.get(
    "/nominal_compositions/",
    response_model=List[schemas.NominalCompositionResponse],
    tags=["CRUD"],
    summary="Lists all NominalCompositions ordered by name.",
    description="Lists all NominalCompositions ordered by name.",
)
def list_nominal_compositions(db: Session = Depends(get_db)):

    ncs = (
        db.query(models.NominalComposition)
        .order_by(models.NominalComposition.name)
        .all()
    )

    return [schemas.NominalCompositionResponse.from_orm(nc) for nc in ncs]


# Update a Nominal Composition entry identified by its name
@router.put(
    "/nominal_compositions/{name}",
    response_model=schemas.NominalCompositionResponse,
    tags=["CRUD"],
    summary="Update a Nominal Composition entry identified by its name.",
    description="Update a Nominal Composition entry identified by its name.",
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


# Deletes a NominalComposition by name.
@router.delete(
    "/nominal_compositions/{name}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["CRUD"],
    summary="Deletes a NominalComposition by name.",
    description="Deletes a NominalComposition by name.",
)
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

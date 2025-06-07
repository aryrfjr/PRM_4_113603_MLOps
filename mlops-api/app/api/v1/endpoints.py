from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from pathlib import Path as FilePath

from app.database import get_db
from app import models, schemas

from datetime import datetime

##########################################################################
#
# Globals
#
##########################################################################

router = APIRouter()

DATA_ROOT = FilePath("/data/ML/big-data-full")

##########################################################################
#
# Helpers
#
##########################################################################

##########################################################################
#
# Endpoints for different resources types and scopes
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
    tags=["CRUD"],
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
    "/nominal_compositions/{name}",
    response_model=schemas.NominalCompositionResponse,
    tags=["CRUD"],
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
    "/nominal_compositions/",
    response_model=List[schemas.NominalCompositionResponse],
    tags=["CRUD"],
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
    "/nominal_compositions/{name}",
    response_model=schemas.NominalCompositionResponse,
    tags=["CRUD"],
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
@router.delete(
    "/nominal_compositions/{name}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["CRUD"],
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


#
# Endpoints scoped to the Data Generation & Labeling (DataOps) phase,
# which includes the following steps:
#
# - Generate (DataOps phase; exploration/exploitation)
# - ETL model (DataOps phase; Feature Store Lite)
#
########################################################################


# Schedules configuration space exploration for a given nominal composition
@router.post(
    "/generate/{nominal_composition}",
    response_model=schemas.GenericStatusResponse,
    status_code=status.HTTP_202_ACCEPTED,
    tags=["DataOps"],
)
def schedule_exploration(nominal_composition: str, db: Session = Depends(get_db)):

    return schemas.GenericStatusResponse(
        message=f"Exploration scheduled for '{nominal_composition}'.",
        status=schemas.Status.SCHEDULED,
    )


# Schedules geometry augmentation (exploitation) for a given nominal composition and runs
@router.post(
    "/generate/{nominal_composition}/{id_run}/augment",
    response_model=schemas.GenericStatusResponse,
    status_code=status.HTTP_202_ACCEPTED,
    tags=["DataOps"],
)  # TODO: set of id_runs and corresponding augmentation types in the request payload
def schedule_augmentation(
    nominal_composition: str, id_run: str, db: Session = Depends(get_db)
):

    return schemas.GenericStatusResponse(
        message=f"Augmentation scheduled for '{nominal_composition}', run '{id_run}'.",
        status=schemas.Status.SCHEDULED,
    )


# Schedules ETL model (DBI building) for a given nominal composition
@router.post(
    "/etl-model",
    response_model=schemas.ETLModelResponse,
    status_code=status.HTTP_202_ACCEPTED,
    tags=["DataOps"],
)
def schedule_etl_model(payload: schemas.ETLModelRequest, db: Session = Depends(get_db)):

    # NOTE: The ETL model is a two step process originally implemented with the
    # scripts 'create_SSDB.py' (for a single NC) and 'mix_SSDBs.py' (for multiple NCs).
    #
    # TODO: update the request payload to meet that reality.

    return schemas.ETLModelResponse(
        message=f"ETL model build scheduled for '{payload.nominal_composition}'.",
        status=schemas.Status.SCHEDULED,
    )


#
# Endpoints scoped to the Model Development (ModelOps) phase,
# which includes the single step:
#
# - Train/Tune (observability or model evaluation in the ModelOps phase)
#
########################################################################


# Schedules model evaluation for a given model and test set.
@router.post(
    "/evaluate",
    response_model=schemas.EvaluateModelResponse,
    status_code=status.HTTP_202_ACCEPTED,
    tags=["ModelOps"],
)
def schedule_model_evaluation(
    payload: schemas.EvaluateModelRequest, db: Session = Depends(get_db)
):

    return schemas.EvaluateModelResponse(
        message=f"Evaluation scheduled for model '{payload.model_name}' on test set '{payload.test_set}'.",
        status=schemas.Status.SCHEDULED,
    )


#
# Miscellaneous
#
########################################################################


@router.get("/ping", response_model=schemas.PingResponse, tags=["Misc"])
def ping():
    return {"message": "PING OK"}

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app import schemas

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
        status=schemas.Status.SCHEDULED.value,
    )

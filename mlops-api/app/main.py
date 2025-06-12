from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import engine, Base
from app import schemas
from .api.v1 import endpoints_crud as v1_endpoints_crud
from .api.v1 import endpoints_dataops as v1_endpoints_dataops
from .api.v1 import endpoints_modelops as v1_endpoints_modelops

#
# Create database tables on startup (optional in dev)
#
#######################################################################

# NOTE: The class Base inherits the attribute metadata from class
#   DeclarativeBase. The attribute metadata is an instance of
#   sqlalchemy.MetaData and it holds information about all the table
#   definitions associated with the models that inherit from Base.
Base.metadata.create_all(bind=engine)

#
# Initialize FastAPI App
#
#######################################################################

API_NAME = "REST API for the MLOps workflow used in Phys. Rev. Materials 4, 113603"

# Define OpenAPI tag groups
tags_metadata = [
    {
        "name": "DataOps",
        "description": "Tasks related to data generation, configuration exploration, augmentation, and ETL/DBI creation.",
    },
    {
        "name": "ModelOps",
        "description": "Tasks related to evaluating trained models on DBI test sets.",
    },
    {
        "name": "CRUD",
        "description": "Create, read, update, and delete operations.",
    },
    {
        "name": "Misc",
        "description": "Miscellaneous.",
    },
]

app = FastAPI(
    title=API_NAME,
    version="1.0.0",
    description="REST API for MLOps tasks like data generation, augmentation, and building feature store (DBIs).",
    openapi_tags=tags_metadata,
)

#
# CORS Middleware (optional for local dev or frontend apps)
#
#######################################################################
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change in production to specific domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
# API Routers
#
#######################################################################
app.include_router(v1_endpoints_crud.router, prefix="/api/v1")
app.include_router(v1_endpoints_dataops.router, prefix="/api/v1")
app.include_router(v1_endpoints_modelops.router, prefix="/api/v1")


#
# Health Check Endpoint
#
#######################################################################
@app.get("/")
def read_root():
    return {
        "message": f"{API_NAME} is running.",
        "status": "OK",
    }


#
# Miscellaneous
#
########################################################################


@app.get("/ping", response_model=schemas.PingResponse, tags=["Misc"])
def ping():
    return {"message": "PING OK"}

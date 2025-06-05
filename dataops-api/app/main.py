from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import engine, Base
from .api.v1 import endpoints as v1_endpoints

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

API_NAME = "DataOps API for the MLOps workflow used in Phys. Rev. Materials 4, 113603"

app = FastAPI(
    title=API_NAME,
    version="1.0.0",
    description="REST API for DataOps tasks like data generation, augmentation, and building feature store (DBIs).",
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
# API Routers
#
#######################################################################
app.include_router(v1_endpoints.router, prefix="/v1", tags=["DataOps API V1"])


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

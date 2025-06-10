import types
import requests
import os
from enum import Enum

##########################################################################
#
# Globals
#
##########################################################################

# NOTE: the environment variables were defined in docker-compose.yml

API_URL = os.getenv("API_URL")
AIRFLOW_API_URL = os.getenv("AIRFLOW_API_URL")

#
# Possible geometric transformations (shear, tension, compression)
#
# Usage Example:
#
# gt = GeometricTransformations.SHEAR_X_IN_Y_DIRECTION
#
# print(gt.label)  # -> "Shear X in Y direction"
# print(gt.index)  # -> 0
# print(gt.name)   # -> "SHEAR_X_IN_Y_DIRECTION"
#
##########################################################################


class GeometricTransformations(Enum):
    SHEAR_X_IN_Y_DIRECTION = ("Shear X in Y direction", 1)
    SHEAR_X_IN_Z_DIRECTION = ("Shear X in Z direction", 2)
    SHEAR_Y_IN_X_DIRECTION = ("Shear Y in X direction", 3)
    SHEAR_Y_IN_Z_DIRECTION = ("Shear Y in Z direction", 4)
    SHEAR_Z_IN_X_DIRECTION = ("Shear Z in X direction", 5)
    SHEAR_Z_IN_Y_DIRECTION = ("Shear Z in Y direction", 6)
    TENSION_X = ("Tension along X", 7)
    COMPRESSION_X = ("Compression along X", 8)
    TENSION_Y = ("Tension along Y", 9)
    COMPRESSION_Y = ("Compression along Y", 10)
    TENSION_Z = ("Tension along Z", 11)
    COMPRESSION_Z = ("Compression along Z", 12)
    TENSION_XYZ = ("Tension along X, Y, and Z", 13)
    COMPRESSION_XYZ = ("Compression along X, Y, and Z", 14)

    def __init__(self, label: str, index: int):
        self._label = label
        self._index = index

    @property
    def label(self):
        return self._label

    @property
    def index(self):
        return self._index


##########################################################################
#
# Helpers
#
##########################################################################


def fetch_nominal_compositions(st_module: types.ModuleType):
    try:
        resp = requests.get(f"{API_URL}/v1/nominal_compositions/")
        if resp.status_code == 200:
            return resp.json()
        else:
            st_module.error(f"Error {resp.status_code}: {resp.text}")
            return []
    except Exception as e:
        st_module.error(f"API Error: {e}")
        return []


def fetch_nominal_composition_exploration_jobs(
    nominal_composition: str, exploitation_info: bool, st_module: types.ModuleType
):
    try:
        resp = requests.get(
            f"{API_URL}/v1/exploration-jobs/{nominal_composition}?exploitation_info={exploitation_info}"
        )
        if resp.status_code == 200:
            return resp.json()
        else:
            st_module.error(f"Error {resp.status_code}: {resp.text}")
            return []
    except Exception as e:
        st_module.error(f"API Error: {e}")
        return []

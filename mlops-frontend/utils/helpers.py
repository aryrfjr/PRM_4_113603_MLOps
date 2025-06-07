import types
import requests
import os

##########################################################################
#
# Globals
#
##########################################################################

# NOTE: the environment variables were defined in docker-compose.yml

API_URL = os.getenv("API_URL")
AIRFLOW_API_URL = os.getenv("AIRFLOW_API_URL")

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

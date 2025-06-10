import streamlit as st
import requests
import pandas as pd

from utils.helpers import (
    fetch_nominal_compositions,
    fetch_nominal_composition_exploration_jobs,
)
from utils.helpers import AIRFLOW_API_URL

##########################################################################
#
# Globals
#
##########################################################################

##########################################################################
#
# Helpers
#
##########################################################################

##########################################################################
#
# Streamlit actions and rendering
#
##########################################################################

st.set_page_config(page_title="Pre-Deployment Exploration DAG", layout="centered")

st.title("Pre-Deployment Exploration DAG")

all_ncs = fetch_nominal_compositions(st)

selected_nc = st.selectbox("Select a Nominal Composition", [c["name"] for c in all_ncs])

selected_n_runs = st.selectbox(
    "Select the number of 100-atom cells to be generated", list(range(1, 6))
)

if st.button("Trigger DAG"):

    dag_id = "pre_deployment_exploration"  # TODO: shouldn't be hardcoded

    api_conf = {"nominal_composition": selected_nc, "num_simulations": selected_n_runs}

    # TODO: Don’t expose Airflow REST API directly to Streamlit; instead, let FastAPI to proxy that.
    #   Keep Streamlit UI-only. All logic (even triggering pipelines) should be routed via FastAPI.
    response = requests.post(
        f"{AIRFLOW_API_URL}/api/v1/dags/{dag_id}/dagRuns",
        auth=("admin", "admin"),
        json={"conf": api_conf},
    )

    # TODO: even when a specific DAG Task fails, it will return 200 since
    #   the DAG was triggered successfully. For instance, it fails for
    #   Zr46Cu46Al8 because there are not available folders.
    if response.status_code == 200:
        st.success(f"DAG triggered successfully! ({response.text})")
    else:
        st.error(f"Failed: {response.text}")

nc_runs_subruns_from_db = fetch_nominal_composition_exploration_jobs(
    selected_nc, False, st
)

if nc_runs_subruns_from_db:
    df = pd.DataFrame(nc_runs_subruns_from_db)
    st.dataframe(df)

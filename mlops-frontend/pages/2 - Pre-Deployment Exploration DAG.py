import streamlit as st
import requests
from utils.helpers import fetch_nominal_compositions
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

    api_conf = {"nominal_composition": selected_nc, "n_runs": selected_n_runs}

    response = requests.post(
        f"{AIRFLOW_API_URL}/api/v1/dags/{dag_id}/dagRuns",
        auth=("admin", "admin"),
        json={"conf": api_conf},
    )

    if response.status_code == 200:
        st.success("DAG triggered successfully!")
    else:
        st.error(f"Failed: {response.text}")

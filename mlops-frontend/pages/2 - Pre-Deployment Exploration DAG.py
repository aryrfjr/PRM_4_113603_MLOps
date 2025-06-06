import streamlit as st
from utils.helpers import fetch_nominal_compositions

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

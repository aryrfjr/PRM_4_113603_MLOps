import streamlit as st
import requests
import pandas as pd

from utils.helpers import fetch_nominal_compositions
from utils.helpers import API_URL

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

st.set_page_config(page_title="Nominal Compositions CRUD", layout="centered")
st.title("Nominal Compositions Manager")

menu = st.sidebar.selectbox("Menu", ["Read", "Create", "Update", "Delete"])

# Create (POST)
if menu == "Create":
    st.subheader("➕ Create New Nominal Composition")
    name = st.text_input("Name")
    description = st.text_area("Description")

    # TODO: Don’t expose Airflow REST API directly to Streamlit; instead, let FastAPI to proxy that.
    #   Keep Streamlit UI-only. All logic (even triggering pipelines) should be routed via FastAPI.
    if st.button("Create"):
        data = {"name": name, "description": description}
        resp = requests.post(f"{API_URL}/v1/nominal_compositions/", json=data)

        if resp.status_code == 201:
            st.success(f"✅ Nominal composition '{name}' created.")
        elif resp.status_code == 409:
            st.warning(f"⚠️ '{name}' already exists.")
        else:
            st.error(f"❌ Error {resp.status_code}: {resp.text}")

# Read (GET) & List (GET)
elif menu == "Read":

    st.subheader("📄 View Nominal Compositions")

    comps = fetch_nominal_compositions(st)

    if comps:
        df = pd.DataFrame(comps)
        st.dataframe(df)

# Update (PUT)
elif menu == "Update":
    st.subheader("✏️ Update Nominal Composition")

    comps = fetch_nominal_compositions(st)
    if comps:
        selected = st.selectbox("Select Composition", [c["name"] for c in comps])
        current = next(c for c in comps if c["name"] == selected)

        name = st.text_input("New Name (optional)", value=current["name"])
        description = st.text_area(
            "New Description", value=current.get("description", "")
        )

        # TODO: Don’t expose Airflow REST API directly to Streamlit; instead, let FastAPI to proxy that.
        #   Keep Streamlit UI-only. All logic (even triggering pipelines) should be routed via FastAPI.
        if st.button("Update"):
            payload = {"name": name, "description": description}
            resp = requests.put(
                f"{API_URL}/v1/nominal_compositions/{selected}", json=payload
            )

            if resp.status_code == 200:
                st.success(f"✅ '{selected}' updated to '{name}'.")
            elif resp.status_code == 404:
                st.error("❌ Composition not found.")
            else:
                st.error(f"❌ Error {resp.status_code}: {resp.text}")

# Delete (DELETE)
elif menu == "Delete":
    st.subheader("🗑️ Delete Nominal Composition")

    comps = fetch_nominal_compositions(st)
    if comps:
        selected = st.selectbox(
            "Select Composition to Delete", [c["name"] for c in comps]
        )

        # TODO: Don’t expose Airflow REST API directly to Streamlit; instead, let FastAPI to proxy that.
        #   Keep Streamlit UI-only. All logic (even triggering pipelines) should be routed via FastAPI.
        if st.button("Delete"):
            resp = requests.delete(f"{API_URL}/v1/nominal_compositions/{selected}")

            if resp.status_code == 204:
                st.success(f"🗑️ '{selected}' deleted.")
            elif resp.status_code == 404:
                st.error("❌ Composition not found.")
            else:
                st.error(f"❌ Error {resp.status_code}: {resp.text}")

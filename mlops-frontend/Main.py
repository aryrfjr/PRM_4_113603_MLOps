import streamlit as st

st.set_page_config(page_title="PRM_4_113603 MLOps", page_icon="⚛️", layout="wide")

st.title("PRM_4_113603 MLOps Streamlit App")

st.markdown(
    "Below is an illustration of the MLOps workflow in terms of the Generate+ETL (GETL) framework used in **Phys. Rev. Materials 4, 113603** (DOI: https://doi.org/10.1103/PhysRevMaterials.4.113603; or the [preprint](https://www.researchgate.net/publication/345634787_Chemical_bonding_in_metallic_glasses_from_machine_learning_and_crystal_orbital_Hamilton_population)):",
    unsafe_allow_html=False,
)

st.image(
    "img/PRM_4_113603_MLOps.drawio.png", caption="MLOPs workflow used in PRM_4_113603"
)

with open("main_body.md", "r") as file:
    readme_content = file.read()

st.markdown(readme_content, unsafe_allow_html=False)

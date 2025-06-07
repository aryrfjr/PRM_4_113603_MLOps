import requests
from airflow.operators.python import PythonOperator
from airflow.exceptions import AirflowFailException
import os

##########################################################################
#
# Globals
#
##########################################################################

# NOTE: the API_URL environment variable was defined in docker-compose.yml
API_URL = os.getenv("API_URL")

##########################################################################
#
# Helpers
#
##########################################################################

##########################################################################
#
# DAG Tasks for different resources types and scopes
#
# TODO: Makes the DAGs configurable via Streamlit triggering. Using
#   for instance 'nc = dag_run.conf.get("nc", "Zr49Cu49Al2")' and
#   importing 'from airflow.models import Variable, DagRun'.
#
##########################################################################

#
# DAG Tasks scoped to the Data Generation & Labeling (DataOps) phase,
# which includes the following steps:
#
# - Generate (DataOps phase; exploration/exploitation)
# - ETL model (DataOps phase; Feature Store Lite)
#
########################################################################


def explore_cells(dag):

    def _explore():

        response = requests.post(
            f"{API_URL}/generate/Zr49Cu49Al2"
        )  # TODO: parametrize NC

        if response.status_code != 202:
            raise AirflowFailException(
                f"Failed to schedule exploration: {response.text}"
            )

        print(response.json())

    return PythonOperator(task_id="explore_cells", python_callable=_explore, dag=dag)


def exploit_augment(dag):

    def _exploit():

        # TODO: that endpoint will be updated to have a set of id_runs and corresponding
        #   augmentation types in the request payload.
        response = requests.post(
            f"{API_URL}/generate/Zr49Cu49Al2/21/augment"
        )  # TODO: parametrize

        if response.status_code != 202:
            raise AirflowFailException(
                f"Failed to schedule augmentation: {response.text}"
            )

        print(response.json())

    return PythonOperator(task_id="exploit_augment", python_callable=_exploit, dag=dag)


def etl_model(dag):

    def _etl():

        # NOTE: The ETL model is a two step process originally implemented with the
        # scripts 'create_SSDB.py' (for a single NC) and 'mix_SSDBs.py' (for multiple NCs).
        #
        # TODO: the request payload of that endpoint with be updated to meet that reality.
        payload = {
            "nominal_composition": "Zr49Cu49Al2",  # TODO: parametrize
            "labeling_type": "ICOHP",
            "interaction_type": "Zr-Cu",
        }

        response = requests.post(f"{API_URL}/etl-model", json=payload)

        if response.status_code != 202:
            raise AirflowFailException(f"Failed to schedule ETL model: {response.text}")

        print(response.json())

    return PythonOperator(task_id="etl_model", python_callable=_etl, dag=dag)


#
# DAG Tasks scoped to the Model Development (ModelOps) phase,
# which includes the single step:
#
# - Train/Tune (observability or model evaluation in the ModelOps phase)
#
########################################################################


def evaluate_model(dag):

    def _evaluate():

        payload = {
            "model_name": "GPR-custom-0.3",  # TODO: parametrize
            "test_set": "Zr49Cu49Al2",
        }

        response = requests.post(f"{API_URL}/evaluate", json=payload)

        if response.status_code != 202:
            raise AirflowFailException(
                f"Failed to schedule model evaluation: {response.text}"
            )

        print(response.json())

    return PythonOperator(task_id="evaluate_model", python_callable=_evaluate, dag=dag)

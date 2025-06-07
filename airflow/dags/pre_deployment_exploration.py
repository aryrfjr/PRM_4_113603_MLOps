from airflow import DAG
from datetime import datetime
from tasks.pre_deployment_tasks import explore_cells, etl_model, evaluate_model

########################################################################
#
# DAG scoped to the Data Generation & Labeling (DataOps) and Model
# Development (ModelOps) phases, which includes the following steps:
#
# - Generate (DataOps phase; exploration)
# - ETL model (DataOps phase; Feature Store Lite)
# - Train/Tune (observability or model evaluation in the ModelOps phase)
#
########################################################################

with DAG(
    dag_id="pre_deployment_exploration",
    start_date=datetime(2024, 1, 1),
    schedule_interval=None,
    catchup=False,
    tags=["explore", "pre-deployment"],
) as dag:
    step_1 = explore_cells(dag)
    step_2 = etl_model(dag)
    step_3 = evaluate_model(dag)

    step_1 >> step_2 >> step_3

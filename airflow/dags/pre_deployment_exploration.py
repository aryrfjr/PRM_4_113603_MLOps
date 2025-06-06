from airflow import DAG
from datetime import datetime
from tasks.pre_deployment_tasks import explore_cells, etl_model, evaluate_model

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

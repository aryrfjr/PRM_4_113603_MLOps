from airflow.operators.python import PythonOperator


def explore_cells(dag):
    def _explore():
        print("Running CMD simulation for new 100-atom cells...")

    return PythonOperator(task_id="explore_cells", python_callable=_explore, dag=dag)


def exploit_augment(dag):
    def _exploit():
        print("Running geometric transformations on existing cells...")

    return PythonOperator(task_id="exploit_augment", python_callable=_exploit, dag=dag)


def etl_model(dag):
    def _etl():
        print("Building DB of interactions and tracking with DVC...")

    return PythonOperator(task_id="etl_model", python_callable=_etl, dag=dag)


def evaluate_model(dag):
    def _evaluate():
        print("Running cross-validation + production scenario validation...")

    return PythonOperator(task_id="evaluate_model", python_callable=_evaluate, dag=dag)

from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.utils import timezone


with DAG(
    dag_id="my_task_dependencies",
    schedule=None,
    start_date=timezone.datetime(2023, 5, 1),
    tags=["DEB", "Skooldio"],
):

    t1 = EmptyOperator(task_id="t1")
    t2 = EmptyOperator(task_id="t2")
    t3 = EmptyOperator(task_id="t3")
    t4 = EmptyOperator(task_id="t4")
    t5 = EmptyOperator(task_id="t5")
    t6 = EmptyOperator(task_id="t6")
    t7 = EmptyOperator(task_id="t7")
    t8 = EmptyOperator(task_id="t8")
    t9 = EmptyOperator(task_id="t9")

    t1 >> t2 >> t3 >> t4 >> t9
    t1 >> t5 >> [t6, t7] >> t8 >> t9
    t2 >> t6
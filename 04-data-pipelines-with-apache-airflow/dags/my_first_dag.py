# One file, One DAG
# filename should be DAG id

from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.utils import timezone # recommend to use timezone from airflow

# there are 3 fundamental parameters for DAG().
with DAG(
    # basic parameters
    dag_id      = "my_first_dag", # dag_id = name of the python file
    schedule    = None,           # schedule = None means the schedule is not set = one-time
    start_date  = timezone.datetime(2023,5,1),
    # additional parameters
    tags = ["DEB","Skooldio"],     # tags is used for user accesessibility 
    catchup = False,
):
    t1 = EmptyOperator(task_id="t1") # variable name (t1) should be the same as task_id (t1)
    t2 = EmptyOperator(task_id="t2")
    t3 = EmptyOperator(task_id="t3")
    t4 = EmptyOperator(task_id="t4")
    t5 = EmptyOperator(task_id="t5")
    t6 = EmptyOperator(task_id="t6")
    t7 = EmptyOperator(task_id="t7")
    t8 = EmptyOperator(task_id="t8")
    t9 = EmptyOperator(task_id="t9")

    #if we don't write any dependency, t1 and t2 will run at the same time
    #if we write dependency like this, t1 will run before t2
    t1>>t2>>t3>>t4>>t9
    t2>>t6>>t8>>t9
    t1>>t5>>[t6,t7]>>t8
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.utils import timezone


def _get_data():
    pg_hook = PostgresHook(
        postgres_conn_id="my_postgres_conn",
        schema="greenery"
    )
    connection = pg_hook.get_conn()
    cursor = connection.cursor()

    sql = """
        select product_id, name, price, inventory from products
    """
    cursor.execute(sql)
    rows = cursor.fetchall()
    for each in rows:
        print(each)

def _dump_data(num1, num2, num3, table: str):
#def _dump_data(table: str):
    pg_hook = PostgresHook(
        postgres_conn_id="my_postgres_conn",
        schema="greenery"
    )
    #dump to the path outside docker
    pg_hook.bulk_dump(table, f"/opt/airflow/data/{table}_export")
    

with DAG(
    dag_id="play_with_airflow_connections_and_hooks",
    schedule=None,
    start_date=timezone.datetime(2023, 5, 1),
    catchup=False,
    tags=["DEB", "2023"],
):

    get_data = PythonOperator(
        task_id="get_data",
        python_callable=_get_data,
    )

    dump_product_data = PythonOperator(
        task_id="dump_product_data",
        python_callable=_dump_data,
        op_args  = [1,2,3],
        op_kwargs={"table": "products"},
    )

# op_args => send value as arguments
# op_kwargs => send keyword as arguments
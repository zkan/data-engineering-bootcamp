from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.utils import timezone

import great_expectations as ge


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


def _dump_data(table: str):
    pg_hook = PostgresHook(
        postgres_conn_id="my_postgres_conn",
        schema="greenery"
    )
    pg_hook.bulk_dump(table, f"/opt/airflow/dags/{table}_export")


def _validate_data():
	columns = ["product_id", "name", "price", "inventory"]
	my_df = ge.read_csv("/opt/airflow/dags/products_export", names=columns, sep="\t")
	results = my_df.expect_column_values_to_be_between(
    	column="price",
    	min_value=0,
    	max_value=100,
	)
	assert results["success"] is True


with DAG(
    dag_id="play_with_airflow_connections_and_hooks",
    schedule=None,
    start_date=timezone.datetime(2023, 5, 1),
    # catchup=False,
    tags=["DEB", "2023"],
):

    get_data = PythonOperator(
        task_id="get_data",
        python_callable=_get_data,
    )

    dump_product_data = PythonOperator(
        task_id="dump_product_data",
        python_callable=_dump_data,
        op_kwargs={"table": "products"},
    )

    validate_data = PythonOperator(
        task_id="validate_data",
        python_callable=_validate_data,
    )

    dump_product_data >> validate_data
FROM --platform=linux/amd64 apache/airflow:2.9.3

RUN pip install --no-cache-dir airflow-provider-great-expectations==0.2.7 \
                               astronomer-cosmos==1.5.1 \
                               dbt-core==1.8.4 \
                               dbt-postgres==1.8.2 \
                               dbt-bigquery==1.8.2

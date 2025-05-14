FROM --platform=linux/${TARGETARCH} apache/airflow:3.0.1-python3.10

RUN pip install --no-cache-dir airflow-provider-great-expectations==0.3.0 \
                               astronomer-cosmos==1.10.0 \
                               dbt-core==1.9.4 \
                               dbt-postgres==1.9.0 \
                               dbt-bigquery==1.9.1

# Scheduling dbt with Airflow

## Getting Started

Before we run Airflow, let's create these folders first:

```sh
mkdir -p ./dags ./config ./logs ./plugins ./tests
```

On **Linux**, please make sure to configure the Airflow user for the docker-compose:

```sh
echo -e "AIRFLOW_UID=$(id -u)" > .env
```

Copy the content in the `env.extra` file to the `.env` file, so that the `.env` file will look similar to this:

```
AIRFLOW_UID=501
_PIP_ADDITIONAL_REQUIREMENTS=astronomer-cosmos==0.6.5 dbt-core==1.5.0 dbt-bigquery==1.5.0
```

## BigQuery Connection

For the Keyfile JSON, we'll copy the content in the keyfile and paste to it.

![BigQuery Connection in Airflow](./assets/bigquery-connection-in-airflow.png)

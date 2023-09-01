# Bootcamp Project

## Day 1

```bash
poetry run python main-postgres.py
```

```bash
poetry run python main-api.py
```

```bash
poetry run python main-sftp.py
```

## Day 2

```bash
poetry run python load_data_to_bigquery.py
```

## Day 3

```bash
poetry run python load_data_to_gcs_then_bigquery.py
```

## Day 4

### คำสั่ง Exec เข้าไปใน Container

```bash
docker compose exec airflow-scheduler bash
```

### คำสั่ง Backfill

ข้อมูล Events

```bash
airflow dags backfill -s 2021-02-01 -e 2021-02-25 greenery_events_data_pipeline
```

ข้อมูล Orders

```bash
airflow dags backfill -s 2021-02-10 -e 2021-02-11 greenery_orders_data_pipeline
```

ข้อมูล Users

```bash
airflow dags backfill -s 2020-01-05 -e 2020-12-26 greenery_users_data_pipeline
```
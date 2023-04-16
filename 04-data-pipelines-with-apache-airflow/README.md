# Data Pipelines with Apache Airflow

เรียนรู้การสร้าง Data Pipelines โดยใช้ Apache Airflow ตั้งแต่อ่านข้อมูล ทำความสะอาดข้อมูล
และโหลดข้อมูลเข้า Data Lake/Data Warehouse อัตโนมัติ เพื่อนำไปวิเคราะห์ข้อมูลต่อไป

## Starting Airflow

Before we run Airflow, let's create these folders first:

```sh
mkdir -p ./dags ./logs ./plugins ./tests
```

On **Linux**, please make sure to configure the Airflow user for the docker-compose:

```sh
echo -e "AIRFLOW_UID=$(id -u)" > .env
```

See [Setting the right Airflow
user](https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html#setting-the-right-airflow-user)
for more detail.

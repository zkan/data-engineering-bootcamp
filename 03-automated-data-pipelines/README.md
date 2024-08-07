# Automated Data Pipelines

เรียนรู้การสร้าง Data Pipelines โดยใช้ Apache Airflow ตั้งแต่อ่านข้อมูล ทำความสะอาดข้อมูล
และโหลดข้อมูลเข้า Data Lake/Data Warehouse อัตโนมัติ เพื่อนำไปวิเคราะห์ข้อมูลต่อไป

## Files/Folders and What They Do

| Name | Description |
| - | - |
| `dags/` | โฟลเดอร์ที่เก็บโค้ด Airflow DAG หรือ Data Pipelines ที่เราสร้างขึ้น |
| `docker/` | โฟลเดอร์ที่เก็บไฟล์ที่เกี่ยวกับการสร้าง Docker Image ที่ใช้ใน Workshop นี้ |
| `pyspark/` | โฟลเดอร์ที่เก็บโค้ด Python ที่ใช้งาน PySpark |
| `.env.spark` | ไฟล์ Environment สำหรับ Spark |
| `docker-compose-with-spark.yml` | ไฟล์ Docker Compose ที่ใช้สำหรับรัน Airflow กับ Spark Cluster บนเครื่อง Host Machine |
| `docker-compose.yml` | ไฟล์ Docker Compose ที่ใช้รัน Airflow ขึ้นมาบนเครื่อง |
| `Makefile` | ไฟล์ที่ช่วยเรา Automate คำสั่งต่าง ๆ ทำความรู้จักเพิ่มเติมได้ที่ [Makefile Tutorial By Example](https://makefiletutorial.com/) |

## Starting Airflow

Before we run Airflow, let's create these folders first:

```sh
mkdir -p ./dags ./config ./logs ./plugins ./tests ./spark-events
```

On **Linux**, please make sure to configure the Airflow user for the docker-compose:

```sh
echo -e "AIRFLOW_UID=$(id -u)" > .env
```

See [Setting the right Airflow
user](https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html#setting-the-right-airflow-user)
for more detail.

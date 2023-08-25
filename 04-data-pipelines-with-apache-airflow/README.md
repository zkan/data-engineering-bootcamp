# Data Pipelines with Apache Airflow

เรียนรู้การสร้าง Data Pipelines โดยใช้ Apache Airflow ตั้งแต่อ่านข้อมูล ทำความสะอาดข้อมูล
และโหลดข้อมูลเข้า Data Lake/Data Warehouse อัตโนมัติ เพื่อนำไปวิเคราะห์ข้อมูลต่อไป

## Files/Folders and What They Do

| Name | Description |
| - | - |
| `dags/` | โฟลเดอร์ที่เก็บโค้ด DAG หรือ Data Pipelines ที่เราสร้างขึ้น |
| `plugins/` | โฟลเดอร์ที่เก็บ Plugins ของ Airflow |
| `config/` | โฟลเดอร์ที่เก็บไฟล์ Configuration อย่างไฟล์ `airflow_local_settings.py` |
| `tests/` | โฟลเดอร์ที่เก็บ Tests |
| `docker-compose.yaml` | ไฟล์ Docker Compose ที่ใช้รัน Airflow ขึ้นมาบนเครื่อง |

## Starting Airflow

Before we run Airflow, let's create these folders first:

```sh
mkdir -p ./dags ./config ./logs ./plugins ./tests
```

On **Linux**, please make sure to configure the Airflow user for the docker-compose:

```sh
echo -e "AIRFLOW_UID=$(id -u)" > .env
```

See [Setting the right Airflow
user](https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html#setting-the-right-airflow-user)
for more detail.

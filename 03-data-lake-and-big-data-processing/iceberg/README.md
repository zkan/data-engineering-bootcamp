# Experimenting with Apache Iceberg, an Open Table Format using PyIceberg

เวิร์คชอปสั้น ๆ สำหรับเรียนรู้การใช้งาน Apache Iceberg ผ่าน PyIceberg ในภาษา Python

To install package dependencies:

```bash
poetry install
```

To create a storage directory:

```bash
mkdir -p catalog
```

To run the code to experiment with Iceberg:

```bash
poetry run python main.py
poetry run python main_gcs.py
```

To clean up the catalog:

```bash
rm -rf catalog/*
poetry run python delete_gcs_folders.py
```

*Note:* The command above requires a keyfile to delete objects in a GCS bucket.

# Data Lake with Google Cloud Storage & Big Data Processing with Apache Spark

เรียนรู้โครงสร้างพื้นฐานสำหรับการจัดการ Big Data โดยไม่ต้องลงทุนโครงสร้างพื้นฐาน
ทางด้านไอทีที่มีค่าใช้จ่ายสูง ด้วยการใช้เครื่องมือบน Google Cloud Storage (GCS)
และไม่ต้องการเขียนโปรแกรมยาก ๆ

## Files/Folders and What They Do

| Name | Description |
| - | - |
| `docker/` | โฟลเดอร์ที่เก็บไฟล์ที่เกี่ยวกับการสร้าง Docker Image ที่ใช้ใน Workshop นี้ |
| `examples/` | โฟลเดอร์ที่เก็บตัวอย่างโค้ดต่าง ๆ เช่น การอัพโหลดข้อมูลขึ้นไปที่ Google Cloud Storage (GCS) |
| `iceberg/` | โฟลเดอร์ที่เก็บโค้ด Python ที่ใช้งาน PyIceberg สำหรับทดลองทำความคุ้นเคยกับ Apache Iceberg, open-source open table format (OTF) |
| `pyspark/` | โฟลเดอร์ที่เก็บโค้ด Python ที่ใช้งาน PySpark |
| `.env.spark` | ไฟล์ Environment สำหรับ Spark |
| `docker-compose.yml` | ไฟล์ Docker Compose ที่ใช้สำหรับรัน Spark Cluster บนเครื่อง Host Machine |
| `Makefile` | ไฟล์ที่ช่วยเรา Automate คำสั่งต่าง ๆ ทำความรู้จักเพิ่มเติมได้ที่ [Makefile Tutorial By Example](https://makefiletutorial.com/) |

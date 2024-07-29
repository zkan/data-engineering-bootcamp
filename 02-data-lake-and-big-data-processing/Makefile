build:
	docker compose build

up:
	docker compose up -d

down:
	docker compose down

bash:
	docker compose exec -it spark-master bash

submit:
	@read -p "Enter PySpark relative path: " pyspark_path; docker exec -ti spark-master spark-submit --master spark://spark-master:7077 /opt/spark/pyspark/$$pyspark_path

pyspark:
	docker compose exec -it spark-master bash pyspark --master spark://spark-master:7077

spark-sql:
	docker compose exec -it spark-master spark-sql --master spark://spark-master:7077

notebook:
	docker compose exec spark-master bash -c "jupyter notebook --ip=0.0.0.0 --port=3000 --allow-root"

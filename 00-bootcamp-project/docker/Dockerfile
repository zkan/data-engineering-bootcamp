FROM deltaio/delta-docker:0.8.1_2.3.0
# FROM deltaio/delta-docker:0.8.1_2.3.0_arm64

USER root

RUN pip install --no-cache-dir great_expectations[sqlalchemy]==0.17.11 \
                               pytest==7.4.0 \
                               faker==19.3.0 \
                               delta-spark==2.3.0 \
                               sqlalchemy==2.0.20 \
                               psycopg2-binary==2.9.7 \
                               python-dotenv==0.21.0 \
                               mypy==0.991 \
                               flake8==6.0.0 \
                               black==24.3.0 \
                               isort==5.12.0 \
                               notebook==6.5.4 \
                               jupyter-server==2.11.2 \
                               boto3==1.34.104

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    rsync && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY ./conf/spark-defaults.conf "$SPARK_HOME/conf/spark-defaults.conf"
COPY ./conf/metrics.properties "$SPARK_HOME/conf/metrics.properties"
COPY ./jars/gcs-connector-hadoop3-latest.jar "$SPARK_HOME/jars/gcs-connector-hadoop3-latest.jar"
ENV SPARK_CONF_DIR="$SPARK_HOME/conf"
ENV SPARK_MASTER="spark://spark-master:7077"
ENV SPARK_MASTER_HOST spark-master
ENV SPARK_MASTER_PORT 7077
ENV PYSPARK_PYTHON python3

# Create and event logging directory to store job logs
RUN mkdir /tmp/spark-events

RUN chmod u+x /opt/spark/sbin/* && \
    chmod u+x /opt/spark/bin/*

ENV PYTHONPATH=$SPARK_HOME/python/:$PYTHONPATH

COPY entrypoint.sh .

ENTRYPOINT ["./entrypoint.sh"]

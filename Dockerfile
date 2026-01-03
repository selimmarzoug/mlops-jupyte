FROM jupyter/datascience-notebook:latest

USER root

# Install Java for PySpark
RUN apt-get update && \
    apt-get install -y --no-install-recommends openjdk-17-jre-headless && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set JAVA_HOME
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64

COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

USER jovyan

# Disable token authentication
RUN mkdir -p /home/jovyan/.jupyter && \
    echo "c.ServerApp.token = ''" >> /home/jovyan/.jupyter/jupyter_server_config.py && \
    echo "c.ServerApp.password = ''" >> /home/jovyan/.jupyter/jupyter_server_config.py

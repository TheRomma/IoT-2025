FROM python:3.11-slim

WORKDIR /app

COPY controller.py /app

RUN pip install influxdb-client paho-mqtt

CMD ["python", "-u", "controller.py"]

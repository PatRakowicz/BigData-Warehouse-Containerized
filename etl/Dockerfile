FROM python:3.10

WORKDIR /app
COPY etl_script.py .

RUN pip install requests mysql-connector-python

CMD ["python", "etl_script.py"]

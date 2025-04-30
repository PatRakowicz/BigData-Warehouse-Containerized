FROM python:3.10
WORKDIR /app
COPY ml_train.py .
RUN pip install --no-cache-dir pandas mysql-connector-python scikit-learn
CMD ["python", "ml_train.py"]

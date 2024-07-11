FROM docker.io/library/python:3.10.6
WORKDIR /app

COPY app.py /app/
COPY models.py /app/
COPY assets /app/assets
COPY cogs /app/cogs
COPY lib /app/lib
COPY data /app/data
COPY requirements.txt /app/

RUN pip install -r requirements.txt

CMD ["python", "app.py"]

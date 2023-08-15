FROM docker.io/library/python:latest
WORKDIR /app

COPY app.py /app/
COPY assets /app/assets
COPY cogs /app/cogs
COPY lib /app/lib
COPY requirements.txt /app/

RUN pip install -r requirements.txt
RUN mkdir /app/logs
RUN touch /app/logs/.log

CMD ["python", "app.py"]

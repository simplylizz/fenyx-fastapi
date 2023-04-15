FROM python:3.11-slim

COPY ./server/requirements.txt /requirements.txt
COPY ./client/requirements.txt /client-requirements.txt
RUN pip install \
    --no-cache-dir \
    -r /requirements.txt \
    -r /client-requirements.txt

COPY . /app
WORKDIR /app

WORKDIR /app/server
#ENTRYPOINT ["uvicorn", "main:app", "--reload"]
ENTRYPOINT ["python3", "main.py"]

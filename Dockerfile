FROM python:3.11-slim

COPY . /app
WORKDIR /app

RUN pip install \
    --no-cache-dir \
    -r server/requirements.txt

RUN pip install \
    --no-cache-dir \
    -r client/requirements.txt

WORKDIR /app/server
ENTRYPOINT ["uvicorn", "main:app", "--reload"]

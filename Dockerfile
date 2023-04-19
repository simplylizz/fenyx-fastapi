FROM python:3.11-slim
#copy requirements files of server and client to the based image directory with new names
COPY ./server/requirements.txt /server-requirements.txt
COPY ./client/requirements.txt /client-requirements.txt
RUN pip install \
    --no-cache-dir \
    -r /server-requirements.txt \
    -r /client-requirements.txt

COPY . /app
WORKDIR /app

WORKDIR /app/server
#ENTRYPOINT ["uvicorn", "main:app", "--reload"]
ENTRYPOINT ["python3", "main.py"]

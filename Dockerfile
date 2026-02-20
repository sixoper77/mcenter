FROM python:3.12-slim

WORKDIR /usr/src/app

RUN apt-get update && apt-get install -y netcat-openbsd && rm -rf /var/lib/apt/lists/*

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt 

COPY . .

RUN sed -i 's/\r$//g' entrypoint.sh
RUN chmod +x entrypoint.sh

WORKDIR /usr/src/app/mcenter

ENTRYPOINT ["sh", "/usr/src/app/entrypoint.sh"]
FROM python:3.10-slim

WORKDIR /code
RUN apt update && apt install -y libpq-dev gcc
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

CMD python manage.py runserver 0.0.0.0:8000

FROM python:3.10-slim

WORKDIR /code
RUN apt update && apt install -y libpq-dev gcc
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code

CMD python manage.py runserver 0.0.0.0:8000

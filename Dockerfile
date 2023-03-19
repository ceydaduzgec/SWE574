FROM python:3.8

ENV PYTHONBUFFERED 1

WORKDIR /app

RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev\
    && apk -U upgrade\
    && apk add --no-cache libffi-dev openssl-dev

COPY  ./requirements.txt .
RUN pip install --upgrade pip
RUN pip3 install --upgrade setuptools

RUN pip install -r requirements.txt

# copy project
COPY . .

CMD python manage.py makemigrations; python manage.py migrate; python manage.py runserver 0.0.0.0:8000

FROM python:3.9-slim-buster

WORKDIR /app

COPY . /app

RUN apk add --no-cache postgresql-libs && \
    apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev && \
    pip install --no-cache-dir -r requirements.txt && \
    apk --purge del .build-deps

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

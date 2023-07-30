FROM python:3.11-alpine

LABEL authors="shahsad"

WORKDIR /usr/src/app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

RUN python manage.py migrate

EXPOSE 8000

ENTRYPOINT ["daphne", "-b", "0.0.0.0", "learn_ease_backend.asgi:application"]
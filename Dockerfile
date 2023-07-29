FROM python:3.11-alpine
LABEL authors="shahsad"

WORKDIR /usr/src/app

COPY requirements.txt .
RUN pip install -r requirements.txt
# copy project
COPY . .

EXPOSE 8000

# set base command daphne -b 0.0.0.0 learn_ease_backend.asgi:application
CMD ["daphne", "-b", "0.0.0.0", "learn_ease_backend.asgi:application"]

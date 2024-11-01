FROM python:3.10-slim-bullseye

ENV PYTHONPATH "${PYTHONPATH}:/app"

WORKDIR /app

COPY requirements.txt .

RUN apt-get update && apt-get install -y \
    libmariadb-dev-compat \
    libmariadb-dev \
    gcc \
    wget \
    gnupg \
    && echo "deb http://apt.postgresql.org/pub/repos/apt bullseye-pgdg main" > /etc/apt/sources.list.d/pgdg.list \
    && wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add - \
    && apt-get update && apt-get install -y postgresql-client-13

RUN pip install -r requirements.txt

COPY . .

RUN pip install watchdog[watchmedo]

CMD watchmedo auto-restart --directory=./ --pattern=*.py --recursive -- python manage.py runserver 0.0.0.0:8000

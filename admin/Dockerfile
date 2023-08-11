FROM python:3.10-slim-buster

ENV PYTHONPATH "${PYTHONPATH}:/app"

WORKDIR /app

COPY requirements.txt .
COPY ../settings.py settings.py

RUN apt-get update && apt-get install -y \
    libmariadb-dev-compat \
    libmariadb-dev \
    gcc

RUN pip install -r requirements.txt

COPY . .

RUN pip install watchdog[watchmedo]

RUN python -m spacy download en_core_web_sm && python -m nltk.downloader punkt averaged_perceptron_tagger wordnet

CMD watchmedo auto-restart --directory=./ --pattern=*.py --recursive -- python manage.py runserver 0.0.0.0:8000

FROM python:3.10-slim-buster

ENV PYTHONPATH "${PYTHONPATH}:/app"

WORKDIR /app

COPY requirements.txt .

RUN apt-get update && apt-get install -y \
    libmariadb-dev-compat \
    libmariadb-dev \
    gcc

RUN pip install -r requirements.txt

COPY . .

RUN python -m spacy download en_core_web_sm && python -m nltk.downloader punkt averaged_perceptron_tagger

CMD ["python", "bot.py"]
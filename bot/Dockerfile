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

CMD ["python", "main.py"]
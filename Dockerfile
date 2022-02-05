FROM python:3.9-slim-buster
MAINTAINER Ya-s-h

ENV PYTHONDONTWRITEBYTECODE=1

COPY requirements.txt .
RUN python -m pip install -r requirements.txt

WORKDIR /app
COPY . .

CMD ["python", "main.py"]
FROM python:3.10-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .
# COPY producer.py producer.py

ENV PYTHONPATH /app

CMD [ "python3","boto.py"]
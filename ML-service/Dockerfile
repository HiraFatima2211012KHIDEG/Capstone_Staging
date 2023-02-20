FROM python:3.10-slim-buster

COPY  ./ML-service ./ML-service
RUN pip3 install -r ML-service/requirements.txt

CMD [ "python3","ML-service/model_deployment.py"]
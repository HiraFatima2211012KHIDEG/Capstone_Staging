FROM python:3.10-slim-buster

COPY  ./ml_service ./ml_service
RUN pip3 install -r ml_service/requirements.txt

CMD [ "python3","ml_service/model_deployment.py"]

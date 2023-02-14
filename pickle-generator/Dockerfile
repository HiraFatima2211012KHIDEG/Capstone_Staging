FROM python:3.10-slim-buster

WORKDIR /app

COPY ./model model
COPY ./pickle-generator pickle-generator
RUN pip install  -r model/requirements.txt

# CMD ["ls"]
# CMD [ "cd", "model"]
# CMD [ "/bin/bash" ]
CMD ["python3", "model/run_train.py"]


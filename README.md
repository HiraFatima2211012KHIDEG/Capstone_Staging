# About sensorsmock serivce
for successful run, first edit `docker-compose.yml` file
to know your aws session token, run this command in terminal:
~~~
aws sts get-session-token --duration-seconds 129600
~~~
then, edit `docker-compose.yml` file as described:
~~~
environment:
      - SMART_THERMO_BUCKET=<your-s3-bucket-name>
      - CARBON_SENSE_URL=http://extract_service:4008/collect_carbon_sense
      - MOISTURE_MATE_URL=http://extract_service:4008/collect_moisture_mate
      - AWS_ACCESS_KEY_ID=<your-access-key-id>
      - AWS_SECRET_ACCESS_KEY=<your-secret-access-key>
      - AWS_SESSION_TOKEN=<your-session-token>
~~~
after setup your session token, run:
~~~
docker compose up
~~~
### extract:

`extract_moisture_carbon_app.py` is a microservice only for post requests.

---

### sensors:
Open terminal in `sensors/` folder
To **run** container, use:
```docker compose up```
To run container in **detached mode**, use `-d`:
```docker compose up -d```
___
### sensorsmock:
`app.py` basically **run** the API on localhost with `port: 3000` and easily accessed by FastAPI built-in **documentation**, run this on browser:
```0.0.0.0:3000/docs```

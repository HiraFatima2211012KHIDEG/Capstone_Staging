# About sensorsmock serivce

### sensors:
Open terminal in `../sensors/` folder

To **run** container, use:

```docker compose up```

To run container in **detached mode**, use `-d`:

```docker compose up -d```
___

### sensorsmock:

`app.py` basically **run** the API on localhost with `port: 3000` and easily accessed by FastAPI built-in **documentation**, run this on browser:

```0.0.0.0:3000/docs```
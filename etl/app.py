import logging

import uvicorn
from fastapi import FastAPI, Request

logger = logging.getLogger()

app = FastAPI()


@app.post("/collect_moisture_mate")
async def collect_moisture_mate(request: Request):
    moisture_data = await request.json()
    logger.info(moisture_data)
    return {"message": "ok"}


@app.post("/collect_carbon_sense")
async def collect_carbon_sense(request: Request):
    carbon_data = await request.json()
    logger.info(carbon_data)
    return {"carbon_data": "ok"}


def run_app():
    logging.basicConfig(level=logging.INFO)
    uvicorn.run(app, host="0.0.0.0", port=4008)


if __name__ == "__main__":
    run_app()

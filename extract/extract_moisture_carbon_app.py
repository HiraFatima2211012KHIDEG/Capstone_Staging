import logging

import uvicorn
from fastapi import FastAPI, Request
logger = logging.getLogger()

app = FastAPI()


@app.post("/collect_moisture_mate")
async def collect_moisture_mate(request: Request):
    """
    Collect moisture data from a request.

    The function extracts the moisture data from the request in JSON format, logs it using the logger object, and returns a response indicating that the data was received.
    
    :param: request (Request): The incoming request object containing the moisture data.
        
    :return: dict: A response indicating that the moisture data was received.
    """
    moisture_data = await request.json()
    logger.info(moisture_data)
    return {"moisture_data": "ok"}


@app.post("/collect_carbon_sense")
async def collect_carbon_sense(request: Request):
    """
    Function to collect carbon data from a carbon sensing device and log it.

    :param request: HTTP request object containing the carbon data.
    :type request: Request

    :return: JSON response indicating the success of data collection.
    :rtype: Dict[str, str]
    """
    carbon_data = await request.json()
    logger.info(carbon_data)
    return {"carbon_data": "ok"}


def run_app():
    """
    Start the application.

    This function configures basic logging for the application and starts a Uvicorn server using the `app` object. The server will listen on host address `0.0.0.0` and port `4008`.
    """
    logging.basicConfig(level=logging.INFO)
    uvicorn.run(app, host="0.0.0.0", port=4008)


if __name__ == "__main__":
    run_app()

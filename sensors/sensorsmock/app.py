import logging

import uvicorn
from fastapi import FastAPI
from sensorsmock.service import SensorService

app = FastAPI()

sensor_service = SensorService()


@app.get("/api/luxmeter/{room_id}")
def get_luxmeter(room_id: str):
    """
    Retrieve the lux meter data for a given room.

    :param room_id: The ID of the room to retrieve the lux meter data for.
    :type room_id: str
    
    :return: The lux meter data for the given room, or an error message if the room does not exist.
    :rtype: dict
    """
    if not sensor_service.is_allowed_room(room_id):
        return {"error": f"Room {room_id} not exists!"}

    data = sensor_service.get_lux_meter_data(room_id)

    return data


@app.post("/api/collect")
def collect():
    """
    Collect and return a message indicating success.

    :return: A message indicating success.
    :rtype: dict
    """
    return {"msg": "ok"}


@app.on_event("startup")
async def startup():
    """
    Start the sensor service asynchronously.

    This function starts the sensor service by calling the `start` method on the `sensor_service` object.
    """
    await sensor_service.start()


def run_app():
    """
    Start the application.

    This function configures basic logging for the application and starts a Uvicorn server using the `app` object. The server will listen on host address `0.0.0.0` and port `3000`.
    """
    logging.basicConfig(level=logging.INFO)
    uvicorn.run(app, host="0.0.0.0", port=3000)


if __name__ == "__main__":
    run_app()

import json

from flask import Flask, Response
from kafka import KafkaConsumer

app = Flask(__name__)


@app.route("/")
def show_data():
    consumer = KafkaConsumer(
        "predicted_data",
        bootstrap_servers=["kafka:29092"],
        auto_offset_reset="earliest",
        enable_auto_commit=True,
        group_id="my-group",
        value_deserializer=lambda m: json.loads(m.decode("utf-8")),
    )

    def generate():
        for message in consumer:
            yield str(message.value) + "<br>"

    return Response(generate(), mimetype="text/html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

from configparser import ConfigParser
from pathlib import Path
from threading import Event
from uuid import uuid4

import paho.mqtt.client as mqtt


def main() -> None:
    config = ConfigParser()
    config_path = Path(__file__).resolve().parents[1] / "config" / "config.ini"
    if not config.read(config_path):
        raise FileNotFoundError(config_path)

    mqtt_host = config["mqtt"]["host"]
    mqtt_port = config.getint("mqtt", "port")
    # Use a unique test topic, separate from real sensor measurements.
    topic = f"test/ingestion-service/{uuid4().hex}"
    payload = "Hallo vom Ingestion Service!"
    received = Event()

    def on_connect(client, _userdata, _flags, reason_code, _properties) -> None:
        if reason_code.is_failure:
            print(f"MQTT-Verbindung fehlgeschlagen: {reason_code}")
            return
        print(f"Verbunden mit {mqtt_host}:{mqtt_port}")
        client.subscribe(topic, qos=1)

    def on_subscribe(client, _userdata, _mid, reason_codes, _properties) -> None:
        if any(code.is_failure for code in reason_codes):
            print(f"Abonnement fehlgeschlagen: {reason_codes}")
            return
        # Publish only after the broker has confirmed the subscription.
        print(f"Abonniert: {topic}")
        client.publish(topic, payload, qos=1, retain=False)
        print(f"Gesendet: {payload}")

    def on_message(_client, _userdata, message: mqtt.MQTTMessage) -> None:
        if message.topic == topic and message.payload == payload.encode("utf-8"):
            print(f"Empfangen: {message.payload.decode('utf-8')}")
            received.set()

    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.on_connect = on_connect
    client.on_subscribe = on_subscribe
    client.on_message = on_message

    client.connect(mqtt_host, mqtt_port, keepalive=30)
    client.loop_start()
    try:
        if not received.wait(timeout=10):
            raise TimeoutError(
                "Keine Testnachricht innerhalb von 10 Sekunden empfangen."
            )
        print("Pub/Sub-Test erfolgreich.")
    finally:
        client.disconnect()
        client.loop_stop()


if __name__ == "__main__":
    main()

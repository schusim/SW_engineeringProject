# Ingestion Service Docker

Run all commands from the **repository root** (`SW_engineeringProject/`).

The current `src/main.py` runs a one-shot MQTT Pub/Sub test and exits afterwards.
Use `docker compose run --rm` for this test. With the current
`restart: unless-stopped` policy, `up -d` would repeatedly restart it.

## Start

### 1. Create shared network
Skip this command if `iot-net` already exists:

```bash
docker network create iot-net
```

### 2. Start the MQTT broker

```bash
docker compose -f mqtt-broker/docker-compose.yml up -d
```

### 3. Build the Ingestion Service image

The build installs `requirements.txt` from the repository root. Rebuild after
changing the Python code or requirements. `DOCKER_BUILDKIT=0` uses the classic
builder so the command also works without the Buildx plugin:

```bash
DOCKER_BUILDKIT=0 docker compose -f ingestion-service/docker-compose.yml build
```

### 4. Run the Python MQTT Pub/Sub test

```bash
docker compose -f ingestion-service/docker-compose.yml run --rm --no-deps --name ingestion-service-pubsub-test ingestion-service
```

The test output appears directly in the terminal. On success, the final lines are:

```text
Gesendet: Hallo vom Ingestion Service!
Empfangen: Hallo vom Ingestion Service!
Pub/Sub-Test erfolgreich.
```

The script reads `config/config.ini`, subscribes to a unique test topic with QoS 1,
and publishes a test message after the broker confirms the subscription. It exits
successfully once the same message is received, or fails after a 10-second receive
timeout. Test messages are not retained. The test container is automatically
removed after it exits; the MQTT broker continues running.

## Stop

The test normally stops automatically. To cancel a running test, press `Ctrl+C`
in its terminal, or run this command in another terminal:

```bash
docker stop ingestion-service-pubsub-test
```

If you previously started the Ingestion Service with `up -d`, stop and remove that
service container before running the one-shot test:

```bash
docker compose -f ingestion-service/docker-compose.yml down
```

Stop and remove the MQTT broker container when it is no longer needed:

```bash
docker compose -f mqtt-broker/docker-compose.yml down
```

The broker's data in `mqtt-broker/data/` and the external network `iot-net` are
preserved. To run the test again, start the broker and repeat the test command.

# MQTT Messages and Topics Specification
One ESP32 or simulator publishes IMU data through Mosquitto to the Python app.

## Topics

IDs are hardcoded: `device_id = esp32-01`, `sensor_id = imu-01`.
All topics from one Sensor use the prefix `sensors/v1/esp32-01/imu/imu-01/`.

| Topic suffix | Direction | Purpose |
|---|---|---|
| `measurements` | Sensor → Python app | IMU readings |
| `errors` | Sensor → Python app | Sensor failures |
| `config` | Python app → Sensor | Set publish rate and synchronise time |
| `config/ack` | Sensor → Python app | Confirm or reject configuration |

A topic routes a message; its payload is a UTF-8 JSON object. Use QoS 1 and `retain=false` for all four topics.

## Measurement

Topic: `sensors/v1/esp32-01/imu/imu-01/measurements`

Example measurement message:

```json
{
  "device_id": "esp32-01",
  "sensor_id": "imu-01",
  "message_counter": 0,
  "boot_counter": 1,
  "timestamp": "2026-11-14T10:15:30.123Z",
  "measurement_type": "acceleration",
  "unit": "m/s^2",
  "value": { "x": 0.12, "y": -0.08, "z": 9.81 },
  "angular_velocity": { "x": 0.50, "y": -0.20, "z": 0.00 }
}
```

| `measurement_type` | Integration stage | `unit` | `value` |
|---|---|---|---|
| `acceleration` | Not integrated | `m/s^2` | Sensor-frame acceleration, including gravity |
| `velocity` | Integrated once | `m/s` | Linear velocity in a fixed local frame |
| `position` | Integrated twice | `m` | Displacement from the local origin |

All types use numeric `x`, `y`, `z` values. `angular_velocity` is required for acceleration messages, in `deg/s` and sensor coordinates; otherwise it may be omitted.

For velocity and position, remove gravity and transform acceleration into a fixed frame before integration. The frame starts aligned with the sensor at rest, with zero velocity and position. Include `reference_id` (e.g. `session-001`) in these messages and change it whenever integration restarts. These estimates may drift; do not treat them as raw acceleration.

## Message counter and timing

Every measurement and sensor error requires:

| Field | Meaning |
|---|---|
| `boot_counter` | Integer starting at `1`; persist across restarts and increment once on each subsequent boot, before publishing |
| `message_counter` | Integer counter: `0`, `1`, `2`, ...; increment by `1` for each new measurement or sensor error |

Measurements and errors share one message counter per `(device_id, sensor_id, boot_counter)`. Monitor both topics to track the sequence. Retries keep the same `message_counter`; reconnects and configuration changes do not reset either counter. After a restart, increment `boot_counter` and reset `message_counter` to `0`. Configuration requests and acknowledgements use `request_id` separately.

- **Missing:** `12 → 14` leaves `13` pending. Mark it lost if it has not arrived after three expected publish intervals.
- **Out of order / duplicate:** an unseen lower message counter is delayed; an already received counter is a duplicate. A higher `boot_counter` starts a new sequence.
- **Early / late:** at 10 Hz, expect one measurement every 100 ms per type. Compare consecutive monotonic receipt times of the same measurement type against `1 / publish_rate_hz`, allowing a tolerance (e.g. 20 ms). Start a new timing baseline after a rate change, clock synchronisation, or reconnect.
- **Timeout:** no measurement for three publish intervals means the stream is overdue; this alone cannot distinguish message loss from a stopped sensor. With synchronised clocks, receipt UTC minus `timestamp` also estimates message age.

## Configuration

Topic: `sensors/v1/esp32-01/imu/imu-01/config`

```json
{
  "request_id": "config-001",
  "publish_rate_hz": 10,
  "time_utc": "2026-11-14T10:15:30.000Z"
}
```

| Field | Meaning |
|---|---|
| `request_id` | Unique, non-empty string linking the request to its acknowledgement |
| `publish_rate_hz` | Positive number of messages per second for each published measurement type; must be supported by the firmware |
| `time_utc` | Current UTC time; the sensor sets its clock to this value on receipt |

Both settings are optional, but at least one must be present. Omitted settings stay unchanged. Validate the complete request before applying it; reject unsupported values without changing settings. The publish rate does not change the internal sampling or integration rate.

Synchronise before publishing timestamped measurements, and send a fresh time after every reconnect. This is approximate synchronisation because of network delay. Use elapsed monotonic time for integration. Use clean MQTT sessions to avoid queuing clock-setting commands while the sensor is offline. Configuration applies until restart; the default publish rate is 10 Hz.

## Configuration acknowledgement

Topic: `sensors/v1/esp32-01/imu/imu-01/config/ack`

```json
{
  "request_id": "config-001",
  "status": "ok",
  "publish_rate_hz": 10,
  "time_utc": "2026-11-14T10:15:30.001Z"
}
```

Echo `request_id`. On success, return `status: "ok"`, the active publish rate, and the current sensor time if synchronised. On failure, return `status: "error"` and a short `message` explaining the rejection. Duplicate requests with the same ID return the previous acknowledgement without applying the configuration again. MQTT delivery acknowledgement alone does not confirm configuration success.

## Sensor error

Topic: `sensors/v1/esp32-01/imu/imu-01/errors`

```json
{
  "device_id": "esp32-01",
  "sensor_id": "imu-01",
  "message_counter": 1,
  "boot_counter": 1,
  "timestamp": "2026-11-14T10:15:31.123Z",
  "code": "IMU_READ_FAILED",
  "message": "Could not read the IMU."
}
```

Codes: `IMU_INIT_FAILED`, `IMU_READ_FAILED`, `IMU_DISCONNECTED`. Do not publish fabricated measurements after a failed read. Before clock synchronisation, errors may omit `timestamp`.

## Basic rules

- IDs in payloads must match the fixed topic IDs. Timestamps use UTC as shown above.
- The Python app ignores duplicates identified by `(device_id, sensor_id, boot_counter, message_counter)`. `boot_counter` must be a positive integer; `message_counter` must be a non-negative integer.
- Reject invalid JSON, mismatched units, and non-finite or non-numeric axis values without stopping the subscriber. Reject invalid configuration on `config/ack` when a valid `request_id` is available; otherwise log it locally.
- On broker failure, log locally, reconnect, and subscribe again. Run either the hardware or simulator for these IDs.

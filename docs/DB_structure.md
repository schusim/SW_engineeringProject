# Database

Within this project, we use [PostgreSQL](https://www.postgresql.org/). To interact with the database we use [PostgREST API](https://docs.postgrest.org/en/v16/). Refer to the official documentation of the API mentioned, as well as the Entity Relationship Diagram below to fully understand how to interact with it.  

## Entity Relationship Diagram 

```mermaid
erDiagram
    device {
        uuid device_id(PK)
        text device_name
    }

    sensor {
        uuid device_id(PK,FK)
        uuid sensor_id(PK)
        text sensor_name
    }

    measurement {
        uuid measurement_id(PK)
        uuid device_id(FK)
        uuid sensor_id(FK)
        timestamptz timestamp
        text measurement_type
        integer boot_counter
        integer message_counter
        jsonb data
    }

    error {
        uuid error_id(PK)
        uuid device_id(FK)
        uuid sensor_id(FK)
        timestamptz timestamp
        integer boot_counter
        integer message_counter
        text code
        text message
    }

    config {
        uuid config_id(PK)
        uuid sensor_id(FK)
        timestamptz timestamp
        int refresh_rate

    }

    device ||--|{ sensor : "contains"
    sensor ||--|{ measurement : "records"
    sensor ||--|{ error : "records"
    sensor ||--|{ config : "records"
```

The composite key `(device_id, sensor_id)` identifies a sensor and is used consistently
for foreign keys and MQTT payload processing.

`measurement.timestamp` stores the timestamp from the MQTT payload.
`measurement.data` stores the `value` object and optional fields such as
`angular_velocity`, `unit`, and `reference_id`. `measurement_type` remains a
separate column so measurements can be queried and filtered easily.

The pair `(boot_counter, message_counter)` identifies one MQTT message within a
device/sensor sequence. Both measurement and error messages must enforce:

```text
UNIQUE (device_id, sensor_id, boot_counter, message_counter)
```

The following MQTT values must satisfy the stated constraints:

- `boot_counter` must be greater than zero.
- `message_counter` must be greater than or equal to zero.
- `error.timestamp` may be `NULL` before clock synchronisation.
- `device.device_id` and `sensor.sensor_id` must match the corresponding MQTT
  topic IDs and payload IDs.
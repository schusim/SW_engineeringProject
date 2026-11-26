CREATE TABLE IF NOT EXISTS device(
    device_id uuid PRIMARY KEY,
    device_name text NOT NULL
);

CREATE TABLE IF NOT EXISTS sensor (
    device_id uuid NOT NULL REFERENCES device(device_id),
    sensor_id uuid NOT NULL,
    sensor_name text,
    PRIMARY KEY (device_id, sensor_id)
);

CREATE TABLE IF NOT EXISTS measurement (
    device_id uuid NOT NULL,
    sensor_id uuid NOT NULL,
    measurement_id uuid NOT NULL,
    PRIMARY KEY (device_id, sensor_id, measurement_id),
    FOREIGN KEY (device_id, sensor_id)
        REFERENCES sensor(device_id, sensor_id),
    timestamp timestamptz,
    measurement_type text,
    boot_counter integer,
    message_counter integer, 
    data jsonb
);

CREATE TABLE IF NOT EXISTS error (
    device_id uuid NOT NULL,
    sensor_id uuid NOT NULL,
    error_id uuid NOT NULL,
    PRIMARY KEY (device_id, sensor_id, error_id),
    FOREIGN KEY (device_id, sensor_id)
        REFERENCES sensor(device_id, sensor_id),
    timestamp timestamptz,
    measurement_type text,
    boot_counter integer,
    message_counter integer, 
    data jsonb
);

CREATE TABLE IF NOT EXISTS config (
    device_id uuid NOT NULL,
    sensor_id uuid NOT NULL,
    config_id uuid NOT NULL,
    PRIMARY KEY (device_id, sensor_id, config_id),
    FOREIGN KEY (device_id, sensor_id)
        REFERENCES sensor(device_id, sensor_id),
    timestamp timestamptz,
    refresh_rate int
);

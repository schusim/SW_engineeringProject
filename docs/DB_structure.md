# Database

Within this project, we use [PostgreSQL](https://www.postgresql.org/). To interact with the database we use [PostgREST API](https://docs.postgrest.org/en/v16/). Refer to the official documentation of the API mentioned, as well as the Entity Relationship Diagram below to fully understand how to interact with it.  

## Entity Relationship Diagram 

```Mermaid
erDiagram

    Sensors {
        integer SensorID(PK)
        text Type
    }

    Sensors ||--|{ Measurements : SensorID

    Measurements {
        integer MeasurementID(PK)
        integer SensorID(FK) 
        jsonb Data 
        timestamptz Timestamp 
        Hash string
    }

```
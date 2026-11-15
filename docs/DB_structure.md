# Database

Within this project, we use [PostgreSQL](https://www.postgresql.org/). To interact with the database we use [PostgREST API](https://docs.postgrest.org/en/v16/). Refer to the official documentation of the API mentioned, as well as the Entity Relationship Diagram below to fully understand how to interact with it.  

## Entity Relationship Diagram 

```mermaid
erDiagram
    Sensors {
        integer SensorID(PK)
        text Name
        text Type
        text Location
        boolean Active
    }

    Measurements {
        integer MeasurementID(PK)
        integer SensorID(FK) 
        timestamptz Timestamp 
        jsonb Data 
        text Hash
    }

    Sensors ||--|{ Measurements : "records"
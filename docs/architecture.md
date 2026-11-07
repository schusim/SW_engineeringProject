# Architecture

## Level 1 Context
```mermaid
flowchart TB
    user["User<br/>[Person]<br/>Wants to view sensor data"]
    sys["Analytics System<br/>[Software System]<br/>Collects, stores and visualizes IMU data"]
    mqtt["MQTT-Broker<br/>[External System]<br/>Mosquitto"]
    iot["IoT-Device generate data"]

    user -->|"Views visualization"| sys
    mqtt -->|"Subscribes / Receives messages"| sys
    iot -->|"publish"| mqtt

    classDef person fill:#08427b,stroke:#052e56,color:#ffffff
    classDef system fill:#1168bd,stroke:#0b4884,color:#ffffff
    classDef external fill:#999999,stroke:#6b6b6b,color:#ffffff
    class user person
    class sys system
    class mqtt external
    class iot external
```
An IoT sensor generates data through measurements. This data is sent to the software system via an MQTT broker. The data is stored in a database. The user can retrieve the data from the database and have it visualized.

## Level 2 Container
```mermaid
flowchart TB
    iot["IoT-Device<br/>[Container: C / Microcontroller]<br/>Publishes IMU sensor data & errors"]
    mqtt["MQTT-Broker<br/>[Container: Mosquitto]<br/>Message broker"]
    
    subgraph server1 ["server 1"]
        collector["Ingestion Service<br/>[Container: Python 3.12]<br/>Subscribes MQTT, handles sensor errors & writes to DB"]
    end

    db[("Database<br/>[Container: SQLite]<br/>Stores measurements & logs")]

    subgraph server2 ["server 2"]
        api["API / Backend Service<br/>[Container: Python 3.12]<br/>Handles user requests"]
        present["Presentation (MPL)<br/>[Container: Python]<br/>Visualizes sensor data"]
    end

    iot -->|"Publish [MQTT]"| mqtt
    mqtt -->|"Messages & Events"| collector
    collector -->|"Insert [SQL]"| db
    db -->|"Query [SQL]"| api
    present -->|"HTTP Request"| api
    api -->|"HTTP Response [JSON]"| present

    classDef container fill:#438dd5,stroke:#2e6295,color:#ffffff
    classDef external fill:#999999,stroke:#6b6b6b,color:#ffffff
    class iot,collector,api,present container
    class mqtt,db external
```
This diagram shows the independent runtime units (containers) of your system and how they are distributed across various devices. The IoT device publishes sensor data and error messages to the central Mosquitto broker via the MQTT protocol. The Ingestion Service receives these messages, processes events, and stores the data persistently in the SQLite database. Separately, the API/Backend Service retrieves the stored data as needed to make it available for visualization via HTTP/JSON.


## Level 3 Component

### MQTT Subscriber
```mermaid
flowchart TB
    subgraph Ingestion ["Ingestion Service [Container: Python 3.12]"]
        config["Config<br/>[Component]<br/>Reads configuration"]
        subscriber["MQTT Subscriber<br/>[Component]<br/>Subscribes to MQTT topic & receives payloads"]
        handler["Event Handler<br/>[Component]<br/>Catches sensor errors & processes events"]
        store["SqliteStore<br/>[Component]<br/>Persists measurements & logs"]
    end

    mqtt["MQTT-Broker<br/>[External System]"] -->|"Messages & Errors"| subscriber
    subscriber --> handler
    handler --> store
    store -->|"SQL Insert"| db[("Database<br/>[SQLite]")]
    config -.->|"Settings"| subscriber
    config -.->|"Settings"| store

    classDef container fill:#438dd5,stroke:#2e6295,color:#ffffff
    classDef component fill:#85bbf0,stroke:#5d82a8,color:#000000
    classDef external fill:#999999,stroke:#6b6b6b,color:#ffffff
    class subscriber,handler,store,config component
    class mqtt,db external
```
The application is a subscriber to the MQTT broker. The data is checked for error messages and stored in the database.

### Backend Handler
```mermaid
flowchart TB
    subgraph ApiService ["API / Backend Service [Container: Python 3.12]"]
        router["HTTP Server / Router<br/>[Component]<br/>Receives HTTP requests"]
        retriever["Data Retriever<br/>[Component]<br/>Queries and prepares data"]
    end

    present["Presentation (MPL)<br/>[External / Client]"] -->|"HTTP Request"| router
    router --> retriever
    retriever -->|"SQL Query"| db[("Database<br/>[SQLite]")]
    db -->|"Raw Data"| retriever
    retriever -->|"HTTP Response [JSON]"| present

    classDef container fill:#438dd5,stroke:#2e6295,color:#ffffff
    classDef component fill:#85bbf0,stroke:#5d82a8,color:#000000
    classDef external fill:#999999,stroke:#6b6b6b,color:#ffffff
    class router,retriever component
    class db,present external
```
The data is retrieved from the database upon a user's request. The data is then formatted for visualization and displayed to the user.

## Level 4 Code
We'll add this once we've started programming.
Zoom into one component. Only draw this level for the important parts, for example your storage interface.
## Dynamic view
```mermaid
sequenceDiagram
    autonumber
    participant IoT as IoT-Device
    participant MQTT as MQTT-Broker
    participant Client as Python Client
    participant DB as SQLite Database
    participant backend as Python backend
    participant MPL as Presentation (MPL)

    IoT->>MQTT: Publish sensor payload (xxx, yyy, zzz...)
    MQTT->>Client: Forward MQTT message
    Client->>DB: Insert measurement (SQL API)
    Note over Client,DB: Data is safely stored over time
    MPL->>backend: HTTP Request for data
    backend->>DB: Query measurements
    DB-->>backend: Return raw data
    backend-->>MPL: HTTP Response (JSON)
    MPL->Render: Render chart for user
```

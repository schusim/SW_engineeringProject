## Sprint 1 (bis 8.11.2026)
**Gut lief:**

Git Projekt wurde erstellt. Die C4-Architektur grob aufgesetzt und das Readme steht. Der Git Workflow wurde definiert. 

Nächste Schritte wurden zugeteilt: 
- Mathias: Abklärungen zu IMU Simulation
- Simon S: ruff und mypy in Git integrieren
- Jan: C4 Diagramm Docker anpassen
- Simon L: Abklärungen zur Datenbank machen
- Florian: mqtt Nachrichten Spezifizieren

**Schlecht lief:**

Nicht ganz alle Merge Request zum main wurden einem Review unterzogen. Es gab noch viele Unklarheiten bezüglich Aufbau des Projektes, nun aber geklärt.

**Änderungen für nächsten Sprint:**

Immer mindestens ein Reviewer in den Merge Request aufnehmen

## Sprint 2 (bis 15.11.2026)
**Gut lief:**

Die C4-Architektur wurde an unsere Besprechungen angepasst. Ruff und mypy wurden in den workflow integriert. Die Mqtt-Nachrichten wurden spezifiziert und erste Abklärungen zur Datenbank und IMU simulation vorgenommen. 

Nächste Schritte wurden zugeteilt: 
- Mathias: Starten IMU Simulation
- Simon S: Starten backend zu Präsentationsschicht
- Jan: Mqtt-Broker in Docker aufsetzen, retro in Git aufnehmen
- Simon L: Starten Datenbank
- Florian: Starten Ingestion Service

**Schlecht lief:**

Unklar ob wenn mehrere Reviewer angewählt werden alle ein Review geben sollen. Wir haben Definiert dass der erste der Zeit hat das Review übernimmt.

**Änderungen für nächsten Sprint:**

Wenn es nicht relevant ist, wer das Review macht, alle Personen als Reviewer anwählen, um Wartezeit auf Review zu verkürzen.

## Sprint 3 (bis 22.11.2026)
**Gut lief:**

Mqtt-Broker wurde aufgesetzt. In allen anderen Programmteilen wurde mit der Implementation gestartet. Mqtt-Brocker soll trozdem eigenen Docker Container erhalten.
Git Pipline mit automatischer Prüfung wurde getestet, Ruff angepasst zur automatischer Formatierung und nicht nur Warnung.

Nächste Schritte wurden zugeteilt: 
- Mathias: weiter IMU Simulation
- Simon S: weiter backend zu Präsentationsschicht
- Jan: README überarbeiten und auf englisch übersetzen
- Simon L: weiter Datenbank
- Florian: weiter Ingestion Service

**Schlecht lief:**

Unklarheiten mit `docker-compose.yml` File sind entstanden -> mehrere sind in unterschiedlichen Ordner entstanden. 

**Änderungen für nächsten Sprint:**

Einzelne `Dockerfile` für die Unterschidlichen Container gemäss `architecture.md` Diagram. Jedoch nur ein zentrales `docker-compose.yml` File für um alle Docker zusammen zu starten.
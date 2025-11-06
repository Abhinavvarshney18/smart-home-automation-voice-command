# smart-home-automation-voice-command
# Abhinav — IoT (ESP32 & Node-RED) Repo

Purpose:
- Focused repo for Avhinav's responsibilities: ESP32 hardware integration, relay wiring, Node-RED automation, MQTT integration and device testing.

Structure:
- esp32/                -> ESP32 Arduino sketch (MQTT relay control)
- node-red/             -> Node-RED flow JSON for automation
- mosquitto/            -> Mosquitto config for local testing
- docker-compose.yml    -> Local dev stack (Mosquitto + Node-RED)
- .github/workflows/ci.yml -> CI: build docker-compose, validate flows

Quick start (PowerShell):
1. Open repo folder:
   cd c:\Users\abhir\Downloads\avhinav-iot
2. Install Docker and Docker Compose (if not installed).
3. Start services for local testing:
   docker-compose up --build -d
4. Flash ESP32 sketch (configure SSID / MQTT broker IP).

Notes:
- This repo is for development/testing only. Secure Mosquitto and production secrets before deployment.
- Each student must use a personal branch (this repo uses `user/avhinav`).

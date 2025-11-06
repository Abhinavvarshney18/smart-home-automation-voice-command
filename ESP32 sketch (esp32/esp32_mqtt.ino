// ESP32 MQTT relay controller (Avhinav)
// Replace WIFI_SSID, WIFI_PASS, MQTT_BROKER_IP
#include <WiFi.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>

const char* WIFI_SSID = "YOUR_SSID";
const char* WIFI_PASS = "YOUR_PASS";
const char* MQTT_BROKER = "192.168.1.100"; // set to host running Mosquitto

WiFiClient espClient;
PubSubClient mqtt(espClient);

const int RELAY_PIN = 2; // change according to board wiring

void connectWiFi() {
  Serial.print("Connecting WiFi");
  WiFi.begin(WIFI_SSID, WIFI_PASS);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nWiFi connected: " + WiFi.localIP().toString());
}

void mqttCallback(char* topic, byte* payload, unsigned int length) {
  // payload is JSON: {"device":"relay1","action":"on"}
  StaticJsonDocument<200> doc;
  DeserializationError err = deserializeJson(doc, payload, length);
  if (err) {
    Serial.println("JSON parse failed");
    return;
  }
  const char* device = doc["device"];
  const char* action = doc["action"];
  Serial.printf("MQTT msg -> device:%s action:%s\n", device, action);
  if (strcmp(action, "on")==0) {
    digitalWrite(RELAY_PIN, LOW); // assume active LOW
  } else if (strcmp(action, "off")==0) {
    digitalWrite(RELAY_PIN, HIGH);
  }
}

void connectMQTT() {
  while (!mqtt.connected()) {
    Serial.print("Connecting MQTT...");
    if (mqtt.connect("esp32-avhinav")) {
      Serial.println("connected");
      mqtt.subscribe("home/commands");
    } else {
      Serial.print("failed: ");
      Serial.print(mqtt.state());
      delay(3000);
    }
  }
}

void setup() {
  Serial.begin(115200);
  pinMode(RELAY_PIN, OUTPUT);
  digitalWrite(RELAY_PIN, HIGH); // off
  connectWiFi();
  mqtt.setServer(MQTT_BROKER, 1883);
  mqtt.setCallback(mqttCallback);
  connectMQTT();
}

void loop() {
  if (WiFi.status() != WL_CONNECTED) connectWiFi();
  if (!mqtt.connected()) connectMQTT();
  mqtt.loop();
}

#include <WiFi.h>
#include <WiFiClient.h>

const char* ssid = "wifi_name";
const char* password = "wifi_password";

const char* host = "192.168.43.246"; // IP address of your Flask server
const int httpPort = 5001; // Port of the Flask server
int key1 = 0;
int key2 = 1;

void setup() {
  Serial.begin(115200);
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }

  Serial.println("Connected to WiFi");

  Serial.print("Connecting to ");
  Serial.println(host);

}

void loop() {
  // Do nothing here
  delay(5000);
  WiFiClient client;

  if (!client.connect(host, httpPort)) {
    Serial.println("Connection failed");
    return;
  }

  String url = "/";
  String postData = "key1=" + String(key1) + "&key2=" + String(key2);
  
  key1++;
  key2++;

  client.println("POST " + url + " HTTP/1.1");
  client.println("Host: " + String(host));
  client.println("User-Agent: ESP32");
  client.println("Connection: close");
  client.println("Content-Type: application/x-www-form-urlencoded");
  client.print("Content-Length: ");
  client.println(postData.length());
  client.println();
  client.println(postData);

  while (client.connected()) {
    String line = client.readStringUntil('\n');
    if (line == "\r") {
      Serial.println("Headers received");
      break;
    }
  }

  String line = client.readStringUntil('\n');
  Serial.println("Reply was:");
  Serial.println("==========");
  Serial.println(line);
  Serial.println("==========");
  Serial.println("Closing connection");
}

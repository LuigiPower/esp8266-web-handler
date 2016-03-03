#include <ESP8266WiFi.h>
#include "WebRequest.h"
#include "IOTNode.h"

const char* ssid = "GdF van #3";
const char* password = "giuggianna";

WebRequest* webHandler;
IOTNode* node;

void setup() {
  Serial.begin(115200);
  Serial.println("Starting setup!");
  delay(10);

  Serial.println("Creating WebRequest");
  webHandler = new WebRequest(ssid, password);
  Serial.println("Creating IOTNode");
  node = new IOTNode(webHandler);
  
  Serial.println("Done setup!");
  
}

void loop() {
  String request = webHandler->receiveRequest();
  
  node->handleRequest(request);
  
  delay(10);
}

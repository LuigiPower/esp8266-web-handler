#include "WebRequest.h"

WebRequest::WebRequest(const char* ssid, const char* password)
{
  server = new WiFiServer(5575);
  
  WiFi.begin(ssid, password);
  
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  
  Serial.println("");
  Serial.println("WiFi connected");
  
  server->begin();
  Serial.println("Server started");
  
  Serial.println(WiFi.localIP());
}

String WebRequest::receiveRequest()
{
  this->client = server->available();
  if (!client) {
    return "NO CLIENT";
  }
  
  // TODO Controllare con timeout?
  // Wait until the client sends some data
  Serial.println("new client");
  while(!client.available()){
    delay(1);
  }
  
  // Read the first line of the request
  String req = client.readStringUntil('\r');
  Serial.println(req);
  client.flush();

  return req;
}

String WebRequest::createHeaders()
{
  String s = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nAccess-Control-Allow-Headers: Content-Type\r\nAccess-Control-Allow-Methods: GET, POST, OPTIONS\r\nAccess-Control-Allow-Origin: *\r\n\r\n ";
  return s;
}

void WebRequest::completeResponse(String partialResponse)
{
  //TODO controllare se chiamare client.flush() qui va bene
  String completeResponse = "<!DOCTYPE HTML>\r\n<html>" + partialResponse + "</html>\n";
  this->sendResponse(completeResponse);
}

void WebRequest::sendResponse(String completeResponse)
{
  String withHeaders = createHeaders() + completeResponse;
  client.print(withHeaders);
  client.flush();
}

String WebRequest::createJSONResponse(String type, String value, String stat, String extras)
{
  String s = "{ type: \"" + type + "\", status:\"" + stat + "\", value: \"" + value + "\", extras: { " + extras + " } }";
  return s;
}


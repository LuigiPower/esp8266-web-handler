#ifndef __WEBREQUEST_H__
#define __WEBREQUEST_H__

#include <ESP8266WiFi.h>

class WebRequest
{
  WiFiServer* server;
  WiFiClient client;
  String ssid;

  virtual String createHeaders();

public:
  WebRequest(const char* ssid, const char* password);

  virtual void sendResponse(String completeResponse);
  virtual void completeResponse(String partialResponse);
  virtual String createJSONResponse(String type, String value, String stat, String extras);
  /**
   * receiveRequest()
   * To be called each on each loop
   * @return String request
   */
  virtual String receiveRequest();

  /**
   * Splits the request
   * @param request request to split
   * @param paramCount where to store the paramCount
   * @return String array
   */
  virtual String* splitRequest(String request, int* paramCount);
};

#endif

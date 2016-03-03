#include "LEDMode.h"

void LEDMode::init(IOTNode* node, JsonObject& json_data)
{
  setOwner(node);
  //TODO do I really have to use JSON?
  gpio = json_data["gpio"];
  
  // prepare GPIO
  pinMode(gpio, OUTPUT);
  digitalWrite(gpio, 0);
}

IOperatingMode* LEDMode::handleRequest(WebRequest* webHandler, String request)
{
  int val;
  if (request.indexOf("/gpio2/0") != -1)
  {
    val = 0;
  }
  else if (request.indexOf("/gpio2/1") != -1)
  {
    val = 1;
  }
  else if(request.indexOf("/dashboard") != -1)
  {
    webHandler->completeResponse("<h1>LED HANDLER</h1><p>I'm an ESP8266 currently in LED mode</p><p>LED should be connected to GPIO2</p><p><a href='gpio2/0'>disable</a></p><p><a href='gpio2/1'>enable</a></p>");
    return NULL;
  }
  else
  {
    return NULL;
  }

  digitalWrite(2, val);
  
  String s = webHandler->createJSONResponse("LED", (val)?"HIGH":"LOW", "SUCCESS", "");
  webHandler->sendResponse(s);
  
  return NULL;
}


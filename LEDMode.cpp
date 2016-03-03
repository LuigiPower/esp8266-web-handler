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
  if (request.indexOf("/gpio/0") != -1)
    val = 0;
  else if (request.indexOf("/gpio/1") != -1)
    val = 1;
  else {
    return NULL;
  }

  digitalWrite(2, val);
  
  String s = webHandler->createJSONResponse("LED", (val)?"HIGH":"LOW", "SUCCESS", "");
  webHandler->completeResponse(s);
  
  return NULL;
}


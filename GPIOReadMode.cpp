#include "GPIOReadMode.h"

void GPIOReadMode::init(IOTNode* node, JsonObject& json_data)
{
  setOwner(node);
  //TODO do I really have to use JSON?
  //gpio = json_data["gpio"];

  // prepare GPIO
  pinMode(2, INPUT);
  pinMode(1, INPUT);
}

IOperatingMode* GPIOReadMode::handleRequest(WebRequest* webHandler, String request)
{
  int val;

  if (request.indexOf("/gpio2") != -1)
  {
    val = digitalRead(2);
  }
  else if (request.indexOf("/gpio1") != -1)
  {
    val = digitalRead(1);
  }
  else if(request.indexOf("/dashboard") != -1)
  {
    webHandler->completeResponse("<h1>GPIO READER</h1><p>I'm an ESP8266 currently in GPIO Read Mode</p><p>Any circuit to be checked should be attached on pin 1 or 2 or both</p><p><a href='gpio1'>Check gpio 1</a></p><p><a href='gpio2'>Check gpio 2</a></p>");
    return NULL;
  }
  else
  {
    return NULL;
  }

  String s = webHandler->createJSONResponse("GPIO", (val)?"HIGH":"LOW", "SUCCESS", "");
  webHandler->sendResponse(s);

  return NULL;
}


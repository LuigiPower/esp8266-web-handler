#include "StartupMode.h"

void StartupMode::init(IOTNode* node, JsonObject& json_data)
{
  setOwner(node);
}

IOperatingMode* StartupMode::handleRequest(WebRequest* webHandler, String request)
{
  if(request.indexOf("/scanning/beacon") != -1)
  {
    webHandler->completeResponse(webHandler->createJSONResponse("BEACON_RESPONSE", "UP", "OK", ""));
    return NULL;
  }
  else if(request.indexOf("/settings/set/mode/ledhandler") != -1)
  {
    webHandler->completeResponse(webHandler->createJSONResponse("CHANGE_STATE", "LED_HANDLER", "OK", ""));
    
    StaticJsonBuffer<200> jsonBuffer;
    JsonObject& root = jsonBuffer.createObject();
    root["gpio"] = 2;

    LEDMode* newmode = new LEDMode();
    newmode->init(this->owner, root);
    return newmode;
  }
  return NULL;
}


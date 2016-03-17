#include "BasicMode.h"

void BasicMode::init(IOTNode* node, JsonObject& json_data)
{
    setOwner(node);
}

IOperatingMode* BasicMode::handleRequest(WebRequest* webHandler, String request)
{
    int argc = -1;
    String* split = webHandler->splitRequest(request, &argc);

    if(checkParam(split, 0, BASIC))
    {
        if(checkParam(split, 1, TEST))
        {
            webHandler->completeResponse("Hello there");
            return NULL;
        }
        else if(checkParam(split, 1, SET) && checkParam(split, 2, MODE))
        {
            if(checkParam(split, 3, GPIO))
            {
                webHandler->sendResponse(webHandler->createJSONResponse("SET_MODE", "GPIO_MODE", "OK", ""));

                StaticJsonBuffer<200> jsonBuffer;
                JsonObject& root = jsonBuffer.createObject();
                //TODO get JSON from request
                root["gpio"] = 2;

                LEDMode* newmode = new LEDMode();
                newmode->init(this->owner, root);
                return newmode;
            }
            else if(checkParam(split, 3, COMPOSITE))
            {
                webHandler->sendResponse(webHandler->createJSONResponse("SET_MODE", "COMPOSITE_MODE", "OK", ""));

                StaticJsonBuffer<0> jsonBuffer;
                JsonObject& root = jsonBuffer.createObject();
                //TODO create empty JSON in a simpler way

                CompositeMode* newmode = new CompositeMode();
                //Need to create a new one, because the old one will be deleted automatically
                newmode->addMode(new BasicMode());

                newmode->init(this->owner, root);
                return newmode;
            }
        }
    }

    return NULL;
}


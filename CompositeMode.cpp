#include "CompositeMode.h"

void CompositeMode::init(IOTNode* node, JsonObject& json_data)
{
    setOwner(node);

    this->modeList = new LinkedList<IOperatingMode*>();
    LinkedList<IOperatingMode*>* pos = this->modeList;

    while(pos->next() != this->modeList)
    {
        IOperatingMode* mode = pos->get();
        mode->init(node, json_data);
        pos = pos->next();
    }
}

IOperatingMode* CompositeMode::handleRequest(WebRequest* webHandler, String request)
{
    int argc = -1;
    String* split = webHandler->splitRequest(request, &argc);

    if(checkParam(split, 0, COMPOSITE))
    {
        if(checkParam(split, 1, ADD) && checkParam(split, 2, MODE))
        {
            if(checkParam(split, 3, BASIC))
            {
                webHandler->sendResponse(webHandler->createJSONResponse("ADD_MODE", "BASIC_MODE", "OK", ""));

                StaticJsonBuffer<0> jsonBuffer;
                JsonObject& root = jsonBuffer.createObject();
                //TODO get JSON from request

                BasicMode* newmode = new BasicMode();
                newmode->init(this->owner, root);
            }
            else if(checkParam(split, 3, GPIO))
            {
                webHandler->sendResponse(webHandler->createJSONResponse("ADD_MODE", "GPIO_MODE", "OK", ""));

                StaticJsonBuffer<200> jsonBuffer;
                JsonObject& root = jsonBuffer.createObject();
                //TODO get JSON from request
                root["gpio"] = 2;

                LEDMode* newmode = new LEDMode();
                newmode->init(this->owner, root);
            }
            else if(checkParam(split, 3, COMPOSITE))
            {
                //TODO doesn't make much sense if I can't choose which modes receive which messages
                webHandler->sendResponse(webHandler->createJSONResponse("ADD_MODE", "COMPOSITE_MODE", "OK", ""));

                StaticJsonBuffer<0> jsonBuffer;
                JsonObject& root = jsonBuffer.createObject();
                //TODO get JSON from request

                CompositeMode* newmode = new CompositeMode();
                newmode->init(this->owner, root);
            }
        }
    }
    else
    {
        LinkedList<IOperatingMode*>* pos = this->modeList;

        while(pos->next() != this->modeList)
        {
            IOperatingMode* mode = pos->get();
            IOperatingMode* newmode = mode->handleRequest(webHandler, request);
            pos = pos->next();

            if(newmode != NULL)
            {
                //If we have to change state, do so immediately: don't complete the cycle
                //chances are that basicmode or similar stuff has been used to change the global state
                //so composite mode has to go
                return newmode;
            }
        }
    }

    return NULL;
}

void CompositeMode::addMode(IOperatingMode* mode)
{
    this->modeList->insert(mode);
}


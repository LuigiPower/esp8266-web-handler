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
    LinkedList<IOperatingMode*>* pos = this->modeList;

    while(pos->next() != this->modeList)
    {
        IOperatingMode* mode = pos->get();
        mode->handleRequest(webHandler, request);
        pos = pos->next();
    }

    return NULL;
}

void CompositeMode::addMode(IOperatingMode* mode)
{
    this->modeList->insert(mode);
}


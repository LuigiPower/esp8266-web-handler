#ifndef __IOPERATINGMODE_H__
#define __IOPERATINGMODE_H__


#include <ArduinoJson.h>
#include "WebRequest.h"
//#include "IOTNode.h"
class IOTNode;

class IOperatingMode
{
  public:
    IOTNode* owner;
    
    virtual ~IOperatingMode() {}
    virtual IOperatingMode* handleRequest(WebRequest* webHandler, String request) = 0;
    virtual void init(IOTNode* node, JsonObject& json_data) = 0;
    
    virtual void setOwner(IOTNode* node)
    {
      this->owner = node;
    }
};

#endif

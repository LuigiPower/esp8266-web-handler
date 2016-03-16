#ifndef __IOPERATINGMODE_H__
#define __IOPERATINGMODE_H__


#include <ArduinoJson.h>
#include "WebRequest.h"
//#include "IOTNode.h"
class IOTNode;

class IOperatingMode
{
    protected:
        const String MODE = "mode";
        const String BASIC = "basic";
        const String GPIO = "gpio";
        const String COMPOSITE = "composite";

        const String TEST = "test";
        const String ADD = "add";
        const String SET = "set";
        const String DEL = "del";

    public:
        IOTNode* owner;

        virtual ~IOperatingMode() {}
        virtual IOperatingMode* handleRequest(WebRequest* webHandler, String request) = 0;
        virtual void init(IOTNode* node, JsonObject& json_data) = 0;

        virtual void setOwner(IOTNode* node)
        {
            this->owner = node;
        }

        virtual bool checkParam(String* params, int which, String check)
        {
            return params[which] == check;
        }
};

#endif

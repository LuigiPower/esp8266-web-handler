#ifndef __BASICMODE_H__
#define __BASICMODE_H__

#include "IOperatingMode.h"
#include "ModeIncludes.h"

class BasicMode : public IOperatingMode
{
    public:
        virtual void init(IOTNode* node, JsonObject& json_data);
        virtual IOperatingMode* handleRequest(WebRequest* webHandler, String request);
};

#endif

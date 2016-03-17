#ifndef __COMPOSITEMODE_H__
#define __COMPOSITEMODE_H__

#include "IOperatingMode.h"
#include "ModeIncludes.h"
#include "LinkedList.h"

class CompositeMode : public IOperatingMode
{
    LinkedList<IOperatingMode*>* modeList;

    public:
        virtual void init(IOTNode* node, JsonObject& json_data);
        virtual IOperatingMode* handleRequest(WebRequest* webHandler, String request);

        virtual void addMode(IOperatingMode* mode);
};

#endif

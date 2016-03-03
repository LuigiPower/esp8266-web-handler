#ifndef __STARTUPMODE_H__
#define __STARTUPMODE_H__

#include "IOperatingMode.h"
#include "LEDMode.h"

class StartupMode : public IOperatingMode
{
  public:
    virtual void init(IOTNode* node, JsonObject& json_data);
    virtual IOperatingMode* handleRequest(WebRequest* webHandler, String request);
};

#endif

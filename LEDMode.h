#ifndef __LEDMODE_H__
#define __LEDMODE_H__

#include "IOperatingMode.h"

class LEDMode : public IOperatingMode
{
  int gpio;
  
  public:
    virtual void init(IOTNode* node, JsonObject& json_data);
    virtual IOperatingMode* handleRequest(WebRequest* webHandler, String request);
};

#endif

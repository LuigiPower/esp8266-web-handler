#ifndef __GPIOREADMODE_H__
#define __GPIOREADMODE_H__

#include "IOperatingMode.h"

class GPIOReadMode : public IOperatingMode
{
  int oldValue = 0;

  public:
    virtual void init(IOTNode* node, JsonObject& json_data);
    virtual IOperatingMode* handleRequest(WebRequest* webHandler, String request);
};

#endif

#ifndef __COMPOSITE_MODE_H__
#define __COMPOSITE_MODE_H__

#include "IOperatingMode.h"

class CompositeMode : public IOperatingMode
{
  int gpio;
  
  public:
    virtual void init(IOTNode* node, JsonObject& json_data);
    virtual IOperatingMode* handleRequest(WebRequest* webHandler, String request);
};

#endif

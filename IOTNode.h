#ifndef __IOTNODE_H__
#define __IOTNODE_H__

#include "IOperatingMode.h"
#include "StartupMode.h"

class IOTNode
{
  IOperatingMode* current_mode = new StartupMode();
  WebRequest* current_server;

public:
  IOTNode(WebRequest* current_server);
  
  IOperatingMode* changeMode(IOperatingMode* mode);
  void handleRequest(String request);
};

#endif

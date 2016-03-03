#include "IOTNode.h"

IOTNode::IOTNode(WebRequest* server)
{
  this->current_server = server;
}

IOperatingMode* IOTNode::changeMode(IOperatingMode* mode)
{
  IOperatingMode* oldmode = this->current_mode;
  this->current_mode = mode;
  return oldmode;
}

void IOTNode::handleRequest(String request)
{
  IOperatingMode* newmode = this->current_mode->handleRequest(this->current_server, request);
  if(newmode != NULL)
  {
    IOperatingMode* oldmode = this->changeMode(newmode);
    delete oldmode;
  }
}


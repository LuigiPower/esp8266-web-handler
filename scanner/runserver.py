#!/usr/bin/env python
from scanner import app
from threading import Thread

print "testing"

handler = None
running = False

def start_flask():
    app.debug = True
    app.run(host='0.0.0.0')

def handler_thread():
    global running
    while running:
        #TODO do stuff like polling the nodes and making notifications
        pass

def start_handler_thread():
    global handler
    global running

    handler = Thread(target = handler_thread)
    running = True
    handler.start()

#TODO weird thread behaviour, is it calling start_flask twice?
start_handler_thread()
start_flask()
running = False

print "All done, closing..."

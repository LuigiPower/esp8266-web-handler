#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pynative.pynative import PyNative
from pynative.views import *
import argparse
import json

pygna = PyNative()

my_name = "esp0"
my_mode = "startup_mode"

def create_json_response(restype, value, status, extras):
    """ Creates a JSON response """
    return {
        'type': restype,
        'value': value,
        'status': status,
        'extras': extras
        }

def create_string_response(restype, value, status, extras):
    response = create_json_response(restype, value, status, extras)
    return json.dumps(response)

@pygna.flask.route('/scanning/beacon')
def beacon():
    print "Received beacon!"
    return create_string_response("BEACON_RESPONSE", "UP", "OK", "")

@pygna.flask.route('/settings/set/mode/<mode>')
def set_mode(mode):
    print "Received SET_MODE request with mode " + mode
    my_mode = mode
    return create_string_response("CHANGE_STATE", mode, "OK", "")

@pygna.flask.route('/gpio<pin>/<highlow>')
def ledmode(pin, highlow):
    print "Received ledmode request gpio%s set to %s" % (pin, highlow)
    result = "HIGH"
    if highlow == "0":
        result = "LOW"
    return create_string_response("LED", result, "SUCCESS", "")

# @pygna.flask.route('/icon/<imagename>')
# def getImage(imagename, imagetype):
# 	return pygna.getImage(imagename, "icon")


@pygna.flask.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    screen = Screen()

    screen.add_view(TextView("Node: %s (Current mode: %s)" % (my_name, my_mode)))

    return pygna.render(screen)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = "Starts an IoTNode emulator (probably better if used with pyco-wrapper)")
    parser.add_argument("-n", "--name", metavar = "name", type = str, required = False, help = "Name of the Node")
    args = parser.parse_args()

    my_name = args.name

    pygna.flask.run(host="0.0.0.0", debug=False)

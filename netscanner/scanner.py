#! python

import netifaces
import httplib
import socket
import json
from netaddr import IPNetwork
from netaddr import IPAddress
from netaddr import iter_iprange
from flask import Flask
from flask import request
from pymongo import MongoClient
from gcm import GCM

API_KEY = "AIzaSyAh1LQr0p_0qB6b4RKhrMr_nxPtjxZfqiI"
PORT_NUMBER = 5575
app = Flask(__name__)
################################################################################

GPIO = "GPIO"

commands = {

}

def getLocalIPs():
    local_ip_addresses = []
    interfaces = netifaces.interfaces()

    for interface in interfaces:
        try:
            for addresses in netifaces.ifaddresses(interface)[netifaces.AF_INET]:
                if addresses['addr'].startswith("127."):
                    continue

                print addresses
                local_ip_addresses.append(addresses)
        except:
            pass

    return local_ip_addresses

def maskToCount(mask):
    count = 0
    for c in mask.bits():
        if c == '1':
            count = count + 1
    return count

def getLocalIPList():
    #TODO farlo funzionare anche se non ho il route a 8.8.8.8
    #networkip = IPNetwork('192.168.1.0/24')

    local_ip_addresses = getLocalIPs()
    iplist = []

    for address in local_ip_addresses:
        count = maskToCount(IPAddress(address['netmask']))
        network = IPNetwork("%s/%d" % (address['addr'], count))
        start = network.network
        end = network.broadcast

        iterator = iter_iprange(start, end)
        for ip in iterator:
            iplist.append(ip)

    return iplist

def scanLocalIPs(iplist):
    esplist = {}

    number = 0

    for ip in iplist:
        try:
            conn = httplib.HTTPConnection(str(ip), PORT_NUMBER, timeout=0.05)
            conn.request("GET", "/scanning/beacon")
            response = conn.getresponse()

            response.read()
            esplist["esp%s" % number] = ip
            number += 1
        except:
            pass

    return esplist

def sendCommand(ip, command):
    conn = httplib.HTTPConnection(str(ip), PORT_NUMBER)
    conn.request("GET", command)
    response = conn.getresponse()
    print response.read()

################################################################################
# MONGO DB INIT
################################################################################

mongodb = MongoClient()
db = mongodb.net_scanner
gcm_collection = db.gcm_collection

def insertGCM(registration_id):
    print "Inserting GCM %s" % registration_id
    element = {
            "registration_id": registration_id
            }
    gcm_collection.insert_one(element)

def removeGCM(registration_id):
    print "Removing GCM %s" % registration_id
    element = {
            "registration_id": registration_id
            }
    gcm_collection.delete_one(element)

################################################################################
# GCM INIT
################################################################################

def sendMessage(reg_id_list, message):
    gcm = GCM(API_KEY)
    data = {'the_message': message}

    print "Received %s" % reg_id_list
    # Downstream message using JSON request
    response = gcm.json_request(registration_ids=reg_id_list, data=data)

    # Downstream message using JSON request with extra arguments
    #res = gcm.json_request(
    #            registration_ids=reg_ids, data=data,
    #                collapse_key='uptoyou', delay_while_idle=True, time_to_live=3600
    #                )

    # Topic Messaging
    #topic = 'topic name'
    #gcm.send_topic_message(topic=topic, data=data)

@app.route('/gcm/registration', methods=['POST'])
def receiveRegistrationId():
    regid = request.form['registration_id']
    print "Received registration id POST: %s" % regid
    insertGCM(regid)
    return "Received registration id %s" % regid

@app.route('/gcm/logout', methods=['POST'])
def removeRegistrationId():
    regid = request.form['registration_id']
    print "To remove registration id POST: %s" % regid
    removeGCM(regid)
    return "Removed registration id %s" % regid

################################################################################
# NETWORK SCAN
################################################################################

print "Scanning network..."

listOfIPs = getLocalIPList()

print "Got interfaces..."
print "Starting network scan (might take a while)..."

#TODO decommentare in futuro
#esplist = scanLocalIPs(listOfIPs)

print "Scan completed."
#print esplist

################################################################################
# SERVER STARTUP
################################################################################

@app.route('/')
def hello_world():
    return "hello world!"

@app.route('/gcm/testmessage')
def send_test_message():
    cursor = gcm_collection.find()
    reg_id_list = []
    for regid in cursor:
        print "Regid found %s" % regid
        reg_id_list.append(regid['registration_id'])

    sendMessage(reg_id_list, "HELLO THERE!")
    return "Test message sent"

@app.route('/node/list', methods=['GET'])
def get_node_list():
    esplist = {
                "esp0": {
                    "ip": "192.168.1.14",
                    "mode": {
                        "name": "gpio_mode",
                        "params": {
                            "gpio": 2
                        }
                    }
                },
                "esp1": {
                    "ip": "192.168.1.74",
                    "mode": {
                        "name": "composite_mode",
                        "params": {
                            "modes": [
                                {
                                    "name": "gpio_mode",
                                    "params": {
                                        "gpio": 1
                                    }
                                },
                                {
                                    "name": "composite_mode",
                                    "params": {
                                        "modes": [
                                            {
                                                "name": "gpio_mode",
                                                "params": {
                                                    "gpio": 2
                                                }
                                            }
                                        ]
                                    }
                                },
                                {
                                    "name": "sticazzi_mode",
                                    "params": {
                                        "sticazziparams": 42
                                    }
                                }
                            ]
                        }
                    }
                }
            }

    tosend = []

    for esp in esplist:
        print "ESP: %s" % esp
        node = esplist[esp]
        tosend.append({ "name": esp, "ip": node['ip'], "mode": node['mode'] })

    return json.dumps(tosend)

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')


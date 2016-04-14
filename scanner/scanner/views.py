from scanner import app
from scanner.mongo import get_gcm_list
from scanner.mongo import insert_gcm
from scanner.iotnodes import Scanner
from scanner.iotnodes import IoTNode
from flask import request
from flask import render_template
import time
import json

#TODO access to this should be regulated by a mutex semaphore, handler thread needs at least read access...
iotscanner = Scanner(init_test = True)
notifier = Notifier()

################################################################################
# NETWORK SCAN
################################################################################

@app.route('/init/scan')
def start_scan():
    print "Starting network scan (might take a while)..."
    iotscanner.run_scan()
    print "Scan completed."
    return str(esplist)

################################################################################

################################################################################
# INDEX
################################################################################

@app.route('/')
def index():
    return render_template('index.html', data=iotscanner.get_node_list())

################################################################################

################################################################################
# GCM TEST
################################################################################

@app.route('/gcm/testmessage')
def send_test_message():
    reg_id_list = get_gcm_list()

    notifier.send_message(reg_id_list, {
            'message': "I'm a GCM message!",
            'event': "VALUE_CHANGED"
        })
    return "Test message sent"

################################################################################

@app.route('/node/list', methods=['GET'])
def show_node_list():
    tosend = get_node_list()
    return json.dumps(tosend)

@app.route('/node/<nodeid>/<action>')
def send_action_to_node(nodeid, action):
    print "Sending %s to %s" % (action, nodeid)
    #TODO send it to the actual node
    return "Sent"

@app.route('/init/testdata')
def load_test():
    return json.dumps(init_test_data())

@app.route('/gcm/registration', methods=['POST'])
def receive_registration_id():
    regid = request.form['registration_id']
    print "Received registration id POST: %s" % regid
    insert_gcm(regid)
    return "Received registration id %s" % regid

@app.route('/gcm/logout', methods=['POST'])
def remove_registration_id():
    regid = request.form['registration_id']
    print "To remove registration id POST: %s" % regid
    remove_gcm(regid)
    return "Removed registration id %s" % regid

@app.route('/door/test', methods=['GET', 'POST'])
def doortesting():
    testdoor()
    return "ciao"

def testdoor():
    i = 0
    while i < 10000:
        result = send_command("192.168.1.76", "/gpio2")
        print "pass %d result %s" % (i, str(result))
        if "HIGH" in result:
            print "HDFIUOHSAFIODSFAHOF"
            send_message(get_gcm_list(), "CIAO MAMMA SONO IN TV")
        #jsonres = json.loads(result)
        #if jsonres['HIGH']:
        #    print "HIIIIIIIIIIGH"
        time.sleep(1)
        i = i + 1

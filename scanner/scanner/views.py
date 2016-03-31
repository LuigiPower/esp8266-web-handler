from scanner import app
from scanner.mongo import get_gcm_list
from scanner.iotnodes import get_node_list
from scanner.iotgcm import send_message
from flask import request
from flask import render_template

################################################################################
# NETWORK SCAN
################################################################################

@app.route('/init/scan')
def start_scan():
    print "Scanning network..."
    listOfIPs = get_local_ip_list()
    print "Got interfaces..."
    print "Starting network scan (might take a while)..."
    esplist = scan_local_ips(listOfIPs)
    print "Scan completed."
    return "OK"

################################################################################

################################################################################
# INDEX
################################################################################

@app.route('/')
def hello_world():
    #TODO check why iotnodes doesn't keep the variable in memory
    return render_template('index.html', data=get_node_list())

################################################################################

@app.route('/gcm/testmessage')
def send_test_message():
    reg_id_list = get_gcm_list()

    send_message(reg_id_list, "HELLO THERE!")
    return "Test message sent"

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


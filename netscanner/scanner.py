import httplib
import socket
from netaddr import IPNetwork

PORT_NUMBER = 5575

def getLocalIP():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('8.8.8.8', 0))
    local_ip_address = s.getsockname()[0]
    return local_ip_address

def getLocalIPList():
    #TODO farlo funzionare anche se non ho il route a 8.8.8.8
    networkip = IPNetwork('192.168.1.0/24')
    iplist = []

    #TODO prendere e considerare la subnetmask
    #TODO per farlo bene, prendere il range tra base e broadcast e farsi il ciclo tra quelli

    baseIp = str(networkip)
    broadcastIp = str(networkip.broadcast)

    #TODO applicare le cose dette sopra, quindi questa cosa va tolta
    tempIp = baseIp[0:baseIp.rfind(".") + 1]

    for i in range(1, 255):
        iplist.append(tempIp + "%s" % i)

    return iplist

def scanLocalIPs(iplist):
    esplist = {}

    number = 0

    for ip in iplist:
        try:
            conn = httplib.HTTPConnection(ip, PORT_NUMBER, timeout=0.05)
            conn.request("GET", "/scanning/beacon")
            response = conn.getresponse()
            #print "GET REQUEST to %s response: %s" % (ip, response.read())
            response.read()
            esplist["esp%s" % number] = ip
            number += 1
        except:
            pass

    return esplist

def setESPMode(ip, mode):
    conn = httplib.HTTPConnection(ip, PORT_NUMBER)
    conn.request("GET", "/settings/set/mode/%s" % mode)
    response = conn.getresponse()
    print response.read()

listOfIPs = getLocalIPList()
esplist = scanLocalIPs(listOfIPs)

if "esp0" in esplist:
    setESPMode(esplist["esp0"], "ledhandler")

print esplist


import netifaces
import httplib
from netaddr import IPNetwork
from netaddr import IPAddress
from netaddr import iter_iprange

################################################################################
# NODE INITIALIZATION
################################################################################
PORT_NUMBER = 5575

GPIO = "GPIO"

commands = {

}

def get_local_ips():
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

def mask_to_count(mask):
    count = 0
    for c in mask.bits():
        if c == '1':
            count = count + 1
    return count

def get_local_ip_list():
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

def scan_local_ips(iplist):
    esplist = {}

    number = 0

    for ip in iplist:
        try:
            conn = httplib.HTTPConnection(ip, PORT_NUMBER, timeout=0.1)
            conn.request("GET", "/scanning/beacon")
            #TODO fare un POST invece di GET, inviando l'ip del server
            #TODO l'ip del server dovrebbe corrispondere all'interfaccia corretta...
            response = conn.getresponse()

            response.read()
            esplist["esp%s" % number] = ip
            number += 1
        except:
            pass

    return esplist

def send_command(ip, command):
    conn = httplib.HTTPConnection(str(ip), PORT_NUMBER)
    conn.request("GET", command)
    response = conn.getresponse()
    print response.read()

################################################################################

################################################################################
# TEST DATA
################################################################################

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



def get_node_list():
    tosend = []

    print "GETTING TEST DATA..."
    print esplist

    for esp in esplist:
        print "ESP: %s" % esp
        node = esplist[esp]
        tosend.append({ "name": esp, "ip": node['ip'], "mode": node['mode'] })

    return tosend


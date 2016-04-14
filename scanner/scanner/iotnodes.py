import netifaces
import httplib
from netaddr import IPNetwork
from netaddr import IPAddress
from netaddr import iter_iprange

################################################################################
# NODE INITIALIZATION
################################################################################

class IOperatingMode(object):
    """ IoTMode helper class
    An IoTMode has it's name and it's parameters
    name is mode type ('gpio_mode', 'composite_mode'...)
    parameters is a dict object containing all it's parameters,
    depending on mode type
    """
    STATUS = 'status'

    def __init__(self, name, parameters):
        self.noderef = None
        self.name = name
        self.parameters = parameters

    def set_node_reference(self, noderef):
        self.noderef = noderef

    def set_parameter(self, key, value):
        """ Set specified parameter to value
        Also notifies any observers
        """
        #TODO notify iotnode so that I can do stuff about it (GCM message, IFTTT....)
        self.parameters[key] = value

    def get_parameter(self, parameter):
        """ Get specified parameter """
        return self.parameters[parameter]

    def to_dict(self):
        """ Gets this mode as a dictionary """
        return {
                'name': self.name,
                'params': self.parameters
            }

    def to_json(self):
        return json.dumps(self.to_dict())

class BasicMode(IOperatingMode):
    """ Basic Mode
    Allows
        /scanning/beacon
        /init/set/mode/<modename>
    """

    def __init__(self):
        super(BasicMode, self).__init__(name = "basic_mode", parameters = {})

class EmptyMode(IOperatingMode):
    """ Empty Mode
    Allows nothing
    """

    def __init__(self):
        super(EmptyMode, self).__init__(name = "empty_mode", parameters = {})

class GPIOMode(IOperatingMode):
    """ GPIO Mode
    Allows
        /gpio<pin>/<value>
    """
    GPIO = 'gpio'

    def __init__(self, pin):
        super(GPIOMode, self).__init__(name = "gpio_mode", parameters = {
                GPIOMode.GPIO: pin,
                IOperatingMode.STATUS: 0
            })

class GPIOReadMode(IOperatingMode):
    """ GPIO Read Mode
    Allows
        /gpio<pin>
    """
    GPIO = 'gpio'

    def __init__(self, pin):
        super(GPIOReadMode, self).__init__(name = "gpio_read_mode", parameters = {
                GPIOReadMode.GPIO: pin,
                IOperatingMode.STATUS: 0
            })

class CompositeMode(IOperatingMode):
    """ Composite Mode
    A container for any number of modes
    can be nested inside other composite modes
    """

    def __init__(self):
        super(CompositeMode, self).__init__(name = "composite_mode", parameters = {
                'modes': []
            })

    def add_mode(self, mode):
        """ Adds a mode to this composite mode """
        self.parameters['modes'].append(mode)

    def _modes_to_dict(self):
        ret = []
        for mode in self.parameters['modes']:
            ret.append(mode.to_dict())
        return ret

    def to_dict(self):
        ret = {
                'name': self.name,
                'params': {
                    'modes': self._modes_to_dict()
                }
            }
        return ret

class IoTNode(object):
    """ IoTNode helper class
    An IoTNode has it's IPAddress, it's name and it's mode
    ip is an IPAddress (or a string)
    name is a string
    mode is an instance of OperatingMode
    values is a dictionary containing node status
    """
    PORT_NUMBER = 5575

    def __init__(self, ip, name, mode):
        self.ip = ip
        self.name = name
        self.mode = mode

        self.mode.set_node_reference(self)

    def send_command(self, command):
        """ Send the specified command to this node
        ex.:
            /gpio1/0
            /gpio1
            /dashboard
            ...
        """
        conn = httplib.HTTPConnection(str(self.ip), PORT_NUMBER)
        conn.request("GET", command)
        response = conn.getresponse()
        return response.read()

    def to_dict(self):
        json = {
                'name': self.name,
                'ip': self.ip,
                'mode': self.mode.to_dict()
            }
        return json

    def to_json(self):
        return json.dumps(self.to_dict())

    def get_value(self, value_name):
        return self.values[value_name]

class Scanner(object):
    ################################################################################
    # TEST DATA
    ################################################################################

    def __init__(self, auto_scan = False, init_test = False):
        self.esplist = {}
        if auto_scan:
            self.run_scan()

        if init_test:
            self._create_test_data()

    def get_node_map(self):
        return self.esplist

    def get_node(self, nodename):
        return self.esplist[nodename]

    def get_json(self):
        return json.dumps(self.get_node_map())

    def _create_test_data(self):
        self.esplist = {}

        gpiomode0 = GPIOMode(2)
        gpiomode0.set_parameter(IOperatingMode.STATUS, 1)
        esp0 = IoTNode('192.168.1.14', 'esp0', gpiomode0)
        self.esplist[esp0.name] = esp0

        compositemode1 = CompositeMode()
        gpiomode11 = GPIOMode(1)
        gpiomode11.set_parameter(IOperatingMode.STATUS, 1)
        compositemode12 = CompositeMode()
        gpiomode12 = GPIOMode(2)
        gpiomode12.set_parameter(IOperatingMode.STATUS, 0)
        compositemode12.add_mode(gpiomode12)
        sticazzimode1 = IOperatingMode("sticazzi_mode", {'sticazziparams': 42})
        compositemode1.add_mode(gpiomode11)
        compositemode1.add_mode(compositemode12)
        compositemode1.add_mode(sticazzimode1)
        esp1 = IoTNode('192.168.1.74', 'esp1', compositemode1)
        self.esplist[esp1.name] = esp1

    def get_node_list(self):
        tosend = []

        for esp in self.esplist:
            print "ESP: %s" % esp
            node = self.esplist[esp]
            tosend.append({ "name": node.name, "ip": node.ip, "mode": node.mode.to_dict() })

        print str(tosend)

        return tosend

    def get_local_ips(self):
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

    def mask_to_count(self, mask):
        count = 0
        for c in mask.bits():
            if c == '1':
                count = count + 1
        return count

    def run_scan(self):
        """ Runs a network scan
        may take a few minutes (does a HTTP request on each device connected to the network)
        """
        iplist = self._get_local_ip_list()
        esplist = self._scan_local_ips(iplist)
        return esplist

    def _get_local_ip_list(self):
        """ Gets list of this server's interfaces
        to get their local ip
        """
        local_ip_addresses = get_local_ips()
        iplist = []

        print "Addresses %s" % str(local_ip_addresses)
        for address in local_ip_addresses:
            count = mask_to_count(IPAddress(address['netmask']))
            network = IPNetwork("%s/%d" % (address['addr'], count))
            start = network.network
            end = network.broadcast

            iterator = iter_iprange(start, end)
            for ip in iterator:
                iplist.append(ip)

        return iplist

    def _scan_local_ips(self, iplist):
        """ Scans given list of networks for ESPs
        or similarly configured HTTP servers
        """
        #TODO magari implementare la cosa che diceva il prof (il nodo fa da server a cui questo si collega per essere configurato. una volta che il nodo e' stato configurato, si passa al normale funzionamento [magari farlo come parametro opzionale? comunque servono 2 interfaccie per fare cio' che dice il prof, per quanto sia essenziale... {in caso staccare momentaneamente il server per collegarsi all'ESP, ma questo tira giu tutto ogni volta che si aggiunge un nodo}])
        esplist = {}

        number = 0

        for ip in iplist:
            try:
                conn = httplib.HTTPConnection(str(ip), PORT_NUMBER, timeout=0.2)
                conn.request("GET", "/scanning/beacon")
                #TODO fare un POST invece di GET, inviando l'ip del server
                #TODO l'ip del server dovrebbe corrispondere all'interfaccia corretta... (basta passarlo insieme alla lista (quindi non passare una lista ma un dizionario in cui a ogni interfaccia corrisponde la sua lista di ip))
                response = conn.getresponse()

                response.read()
                print "FOUND ESP"
                #TODO esp must give back name and current mode(s)
                esplist["esp%s" % number] = ip
                number += 1
            except :
                pass

        return esplist

################################################################################
#   EXAMPLE DATA
#
#    esplist = {
#            "esp0": {
#                "ip": "192.168.1.14",
#                "mode": {
#                    "name": "gpio_mode",
#                    "params": {
#                        "gpio": 2,
#                        "status": 1
#                    }
#                }
#            },
#            "esp1": {
#                "ip": "192.168.1.74",
#                "mode": {
#                    "name": "composite_mode",
#                    "params": {
#                        "modes": [
#                            {
#                                "name": "gpio_mode",
#                                "params": {
#                                    "gpio": 1,
#                                    "status": 1
#                                }
#                            },
#                            {
#                                "name": "composite_mode",
#                                "params": {
#                                    "modes": [
#                                        {
#                                            "name": "gpio_mode",
#                                            "params": {
#                                                "gpio": 2,
#                                                "status": 0
#                                            }
#                                        }
#                                    ]
#                                }
#                            },
#                            {
#                                "name": "sticazzi_mode",
#                                "params": {
#                                    "sticazziparams": 42
#                                }
#                            }
#                        ]
#                    }
#                }
#            }
#        }
#
################################################################################

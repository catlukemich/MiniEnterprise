import socket
from . import inet_constants
from . import endpoint

class Client(endpoint.Endpoint):


    def do_init(self):
        asocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try: 
            asocket.connect((inet_constants.host, inet_constants.port))
            self.conn = asocket
        except TimeoutError:
            return False
        return True
        

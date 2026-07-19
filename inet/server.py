import globs

import socket
from . import endpoint
from . import inet_constants



class Server(endpoint.Endpoint):

    # BIND TIMEOUT - time for the server to bind to the socket
    def do_init(self, bind_timeout):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.bind((inet_constants.host, inet_constants.port))
        except OSError:
            return False
        s.listen(1)

        s.settimeout(bind_timeout)
        conn, address = s.accept()
        self.conn = conn
        return True
    
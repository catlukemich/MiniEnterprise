from . import endpoint


class NullEndpoint(endpoint.Endpoint):

    def send(self, data):
        pass

    def recv(self):
        return []
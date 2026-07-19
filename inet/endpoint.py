import socket

from . import inet_constants


class Endpoint:

    def __init__(self):
        self.conn : socket.socket = None

    def send(self, data):
        if len(data) < 150:
            data += " " * (150 - len(data) - len(inet_constants.END))
        self.conn.send(bytes(data + inet_constants.END, encoding="utf-8"))

    def recv(self):
        self.conn.setblocking(False)
        try:
            raw_data = self.conn.recv(150)
            str_data = str(raw_data, encoding="utf-8")
            messages = str_data.split(inet_constants.END)
            return messages
        except BlockingIOError:
            return []
        
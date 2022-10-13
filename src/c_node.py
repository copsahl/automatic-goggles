# Node class (Compromised Host)
# TODO: RECV will hang if connection gets interrupted while in shell, fix it

from src.c_color import Color
from enum import Enum
from io import BlockingIOError
import random
import socket

class Status(Enum):
    DEAD = 0
    LISTENING = 1
    CONNECTED = 2
    IN_MISSION = 3

'''Base Node'''
class BaseNode:

    def __init__(self, addr: str, port: int):

        self.addr = addr
        self.port = port
        self.name = str(random.randrange(1000, 9999))
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.last_ran = ''
        self.status = Status.DEAD
        self.script = None
        self.tags = []

    def run_cmd(self, cmd: str):
        self._send_msg(cmd)
        self.last_ran = self._get_msg(4096)

    def _get_msg(self, buff_size):
        # NOTE: Make this more cohesive
        data = ''
        try:
            while True:
                data += self.sock.recv(buff_size).decode()
        except socket.timeout:
            return data

    def _send_msg(self, msg):
        try:
            self.sock.send(f"{msg}\n".encode())
        except BrokenPipeError as e:
            print(f"Ope: {e}. Message '{msg}' failed to send.")

    def close(self):
        if self.sock:
            self.sock.close()
            self.status = Status.DEAD
            return 0
        return -1

    def add_tag(self, tag):
        if tag not in self.tags:
            self.tags.append(tag)

    def del_tag(self, tag):
        if tag in self.tags:
            self.tags.remove(tag)


'''Connect Node'''
class CNode(BaseNode):

    def __init__(self, addr: str, port: int):
        BaseNode.__init__(self, addr, port)

    def start(self):
        try:
            self.sock.connect((str(self.addr), int(self.port)))
        except (ConnectionRefusedError, BlockingIOError):
            return -1

        self.status = Status.CONNECTED
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.settimeout(0.2)

'''Listen Node (Reverse shell)'''
class LNode(BaseNode):

    def __init__(self, port: int):
        BaseNode.__init__(self, "0.0.0.0", port)
        self.l_sock = None

    def start(self):

        try:
            self.l_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.l_sock.bind((self.addr, self.port))
            self.status = Status.LISTENING
            self.l_sock.listen(3)
            self.sock, self.addr = self.l_sock.accept()
            self.l_sock.close()
        except:
            return -1

        self.status = Status.CONNECTED
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.settimeout(0.2)

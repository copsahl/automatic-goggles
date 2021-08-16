# TODO: Add file upload
# TODO: Make autostart a background process 

from cmd import Cmd
from datetime import datetime
import random
from src.c_node import *
from src.c_color import *
from multiprocessing import Process
from os import system, listdir, path
from pprint import pprint
from sys import platform

class Manager(Cmd):

    prompt = f"[{Color.YELLOW}~{Color.END}] "
    intro = f"type 'help' for commands"

    def __init__(self):
        Cmd.__init__(self)
        self.node_dict = {}
        self.cmd_history = {}
        self.threads = []

    def do_help(self, intro=None):
        print('''
    connect <ip> <port>     - Connect to remote shell at <ip>:<port>
    listen <port>           - Set up listening node for incoming reverse shells

    list                    - List All Nodes
    status <node>           - Get the status of a specific node (DEAD, LISTENING, CONNECTED)
    info <node>             - Get basic information of a given node connection. (Hostname, current user, os version)
    shell <node>            - Drop into a shell on the given node and run commands manually.

    scripts                 - List all available scripts in 'automation/windows' and 'automation/linux'
    assign <node> <script>  - Assign a given script to a given node. Script should be in the form of 'linux/my_script' or 'windows/my_script'
    autostart <node>        - Start the automation mission for a given node that has a script assigned to it. 

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

    def _listen(self, args):
        pass

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
            filename  = f"{d.strftime('%B-%d-%Y-%H_%M')}.dat"
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

        for t in self.threads:
            t.kill()    # Act very harshly towards our created processes for the mean time 
        print("Exiting...")
        exit(0)

    def do_clear(self, args):
        if "win" in platform.lower():
            system("cls")
        else:
            system("clear")

    def do_scripts(self, arg):
        if not arg:
            try:
                print("--Windows Scripts--")
                for script in listdir(path.join("automation", "windows")):
                    print(f"\t{script}")
                print("--Linux Scripts--")
                for script in listdir(path.join("automation", "linux")):
                    print(f"\t{script}")
            except:
                print("Ope: Failed to find files. Are they in 'automation/(windows|linux)'")

    def do_assign(self, args):
        """Script syntax should be 'linux/<script>' so we know which os"""
        if not args:
            print("Ope: Invalid Syntax!")
            return
        try:
            node_name, script = args.split()
            node = self.get_node(node_name)
        except:
            print("Ope: Invalid Syntax")
        
        node.script = f"automation/{script}"
        print(f"Script '{script}' assigned to node '{node.name}'")

    def do_autostart(self, args):
        data = {}
        """Start automation mission"""
        if not args:
            print("Ope: Invalid Syntax! Expected 'node'.")
            return
        
        node = self.get_node(args)
        if not isinstance(node, (CNode, LNode)):
            print("Ope: Not a valid node!")
            return
        
        node.status = Status.IN_MISSION
        if node.script == None:
            print("Ope: Node doesn't have an assigned script!")
            return

        with open(node.script) as s:
            lines = s.readlines()
        node.sock.settimeout(1)
        for line in lines:
            node.run_cmd(line.strip())
            data[line] = node.last_ran
        node.sock.settimeout(0.2)
        node.script = None  # Remove script
        d = datetime.now()
        filename  = f"NODE{node.name}_MISSION{d.strftime('%B-%d-%Y-%H_%M')}.dat"
        with open(filename, "wt") as fObj:
            pprint(data, stream=fObj)
        print("Mission Finished and exported!")
        node.status = Status.CONNECTED

    def get_node(self, name):
        try:
            return self.node_dict[name]
        except KeyError:
            print(f"Ope: '{name}' not found.")
            return None

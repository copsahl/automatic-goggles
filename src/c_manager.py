# TODO: Add file upload
from src.c_node import *
from src.c_color import *
from pprint import pprint

class Manager:

    def __init__(self):
        self.node_dict = {}
        self.cmd_history = {}

    def create_node(self, conn, conn_type=ConnType.TCP_CONN):
        new_node = Node(conn[0], conn[1], conn_type=conn_type)
        if new_node.name in self.node_dict:
            new_node.name = str(int(new_node.name) + 1)
        self.node_dict[new_node.name] = new_node
        if new_node.start() == -1:
            print("Failed to start node!")
            del self.node_dict[new_node.name]
            return None
        self.node_dict[new_node.name] = new_node
        return new_node

    def get_node(self, name):
        try:
            return self.node_dict[name]
        except KeyError:
            print(f"Ope: '{name}' not found.")

    def shell(self, node, hist=False):
        if not isinstance(node, Node):
            print("Ope: Invalid node, cannot switch to shell...")
            return
        print(f"Dropping into shell on '{node.name}'.")
        while True:
            try:
                command = input("[\033[91m~\033[0m] ")
            except KeyboardInterrupt:
                print("\nExiting shell...")
                return
            if command in ['quit', 'exit']:
                return
            node.run_cmd(command.strip())
            print(node.last_ran, end="")
            if hist:
                self.cmd_history[command.strip()] = node.last_ran
    
    def get_cmd_history(self):
        pprint(self.cmd_history)

    def export_cmd_history(self, filename):
        with open(filename, "wt") as fObj:
            pprint(self.cmd_history, stream=fObj)
        print("Session exported to file!")

    def list_nodes(self):
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

    def node_info(self, node):
        try:
            node.collect()
        except:
            print("Ope: Collection failed!")
            return

        print(f"Name: {node.name}")
        print(f"Network: {node.addr}:{node.port} -- {node.conn_type}")
        print(f"Hostname: {node.hostname}")
        print(f"Current User: {node.user}")
        print(f"Operating System: {node.os}")
        print(f"Status: {node.status}")
    
    def node_status(self, node):
        if node.status == Status.DEAD:
            print(f"{Color.RED}STATUS: node '{node.name}' is DEAD.{Color.END}")
        elif node.status == Status.LISTENING:
            print(f"{Color.CYAN}STATUS: node '{node.name}' is LISTENING.{Color.END}")
        elif node.status == Status.CONNECTED:
            print(f"{Color.GREEN}STATUS: node '{node.name}' is CONNECTED.{Color.END}")
    
    def close(self, node):
        node.close()

    def close_all(self):
        for k, v in self.node_dict.items():
            v.close()

    def remove_node(self, node):
        try:
            del self.node_dict[node.name]
            print("Node successfully removed!")
        except:
            print("Ope: Failed to delete node from list")

    def remove_all(self):
        self.node_dict.clear()
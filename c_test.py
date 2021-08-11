import cmd
from c_node import *
from c_color import *
from c_manager import *

class Menu(cmd.Cmd, Manager):

    def __init__(self):
        Manager()

    def do_connect(self, args):
        if args[0] in self.node_dict:
            print(f"Ope: '{args[0]}' already taken.")
            return None
        new_node = Node(args[1], args[2], name=args[0], conn_type=args[3])
        self.node_dict[new_node.name] = new_node
        if new_node.start() == -1:
            print("Failed to start node!")
            del self.node_dict[new_node.name]
            return None
        self.node_dict[new_node.name] = new_node
        return new_node
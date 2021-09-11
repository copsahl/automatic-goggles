from src.c_node import *
from src.c_manager import *
from src.c_color import *
from os.path import exists
import json

class Error(Exception):
    pass

class JSONConfigFileNotFound(Error):
    pass

class Loader:

    """Class to load JSON configuration file for automatic node creation"""

    @staticmethod
    def json_load(local_file, node_dictionary):
        print(f"Attempting to load node-configurations/{local_file}...")
        if not exists(f"node-configurations/{local_file}"):
            raise JSONConfigFileNotFound

        with open(f"node-configurations/{local_file}") as fObj:
            data = fObj.read()

        parsed_json = json.loads(data)

        for k, v in parsed_json.items():
            for node_item in v:
                addr = str(node_item["ip"])
                port = int(node_item["port"])

                # now just create a node for each thing in our JSON soup
                new_node = CNode(addr, port)
                new_node.name = str(node_item["node_id"])

                # add it to the node dictionary from c_manager
                node_dictionary[new_node.name] = new_node

                if new_node.start() == -1:
                    print(f"{Color.RED}Ope: Unable to connect to {addr}:{port}!{Color.END}")
                    del node_dictionary[new_node.name]

        return 0

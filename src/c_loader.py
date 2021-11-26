from src.c_node import *
from src.c_manager import *
from src.c_color import *
from os.path import exists
import json

class Error(Exception):
    pass

class JSONConfigFileNotFound(Error):
    pass

class JSONConfigSaveError(Error):
    pass

class Loader:

    """Class to load JSON configuration file for automatic node creation"""

    @staticmethod
    def json_load(local_file, node_dictionary, thread_list):
        '''
            Loads a JSON node configuration file in the node-configurations directory
            and attempts to connect to each node.
            Example configuration:
            {
                "nodes": [
                    {
                        "node_id": 1337,
                        "node_type": "cnode",
                        "ip": "127.0.0.1",
                        "port": 1337
                    },
                    {
                        "node_id": 1338,
                        "node_type": "lnode",
                        "port": 4444
                    }
                ]
            }
        '''

        print(f"Attempting to load node-configurations/{local_file}...")
        if not exists(f"node-configurations/{local_file}"):
            raise JSONConfigFileNotFound

        with open(f"node-configurations/{local_file}") as fObj:
            data = fObj.read()

        parsed_json = json.loads(data)

        for k, v in parsed_json.items():
            for node_item in v:
                # Check node type (cnode or lnode)
                new_node_type = str(node_item["node_type"])
                if "cnode" in new_node_type:
                    # If the node is a cnode, it needs an addr and a port
                    new_node_addr = str(node_item["ip"])
                    new_node_port = int(node_item["port"])
                    # Create the new node
                    new_node = CNode(new_node_addr, new_node_port)
                    new_node.name = str(node_item["node_id"])
                    node_dictionary[new_node.name] = new_node

                    if new_node.start() == -1:
                        print(f"{Color.RED}Ope: Unable to connect to {new_node_addr}:{new_node_port}!{Color.END}")
                        del node_dictionary[new_node.name]

                elif "lnode" in new_node_type:
                    # If the node is an lnode, it only needs a port
                    new_node_port = int(node_item["port"])
                    # Create the new node
                    new_node = LNode(new_node_port)
                    new_node.name = str(node_item["node_id"])
                    node_dictionary[new_node.name] = new_node

                    # We might want to have a function for listening that does error checking,
                    # and then use that as the target for the thread
                    t = threading.Thread(target=new_node.start(), args=(args, ), daemon=True)
                    thread_list.append(t)
                    t.start()

                    if new_node.start() == -1:
                        print(f"{Color.RED}Ope: Unable to listen on {new_node_port}!")
                        del node_dictionary[new_node.name]
                else:
                    # Node type must be either cnode or lnode
                    print(f"{Color.RED}Ope: Invalid node type '{new_node_type}' specified!{Color.END}")
                    return -1

            return 0

    @staticmethod
    def json_save(local_file, node_dictionary):
        '''
            Saves the current node configuration to a JSON file in the node_configurations directory.
        '''

        json_export_dict = {
            "nodes": []
        }

        for k, v in node_dictionary.items():
            # Set fields for the JSON file that we're going to save
            saved_node_id = k

            # If the node in the dictionary is an LNode
            if isinstance(v, LNode):
                saved_node_type = "lnode"
                saved_node_port = v.port
                new_dict = {
                    "node_id": saved_node_id,
                    "node_type": saved_node_type,
                    "port": saved_node_port
                }
            else:
                saved_node_type = "cnode"
                saved_node_ip = v.addr
                saved_node_port = v.port
                new_dict = {
                    "node_id": saved_node_id,
                    "node_type": saved_node_type,
                    "ip": saved_node_ip,
                    "port": saved_node_port
                }


            json_export_dict["nodes"].append(new_dict)


        print(f"Attempting to save node-configurations/{local_file}...")

        with open(f"node-configurations/{local_file}", "w") as fObj:
            json.dump(json_export_dict, fObj)

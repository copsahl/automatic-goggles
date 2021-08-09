#!/usr/bin/env python3
import shutil
from c_color import *
from os import system as s
from c_manager import *

# TODO: Have configuration file that allows for nodes to be preconfigured. 
def main():

    columns = shutil.get_terminal_size().columns
    printc("automatic goggles", columns)
    printc("chase opsahl", columns)
    print()

    menu()

def printc(string, size):
    print(string.center(size))

def menu():
    m = Manager()
    while True:
        cmd = input(f"[{Color.YELLOW}~{Color.END}] ")

        spl_cmd = cmd.split(' ')
        if spl_cmd[0] == 'connect':
            if spl_cmd[4] == "TCP_CONN":
                m.create_node(spl_cmd[1], (spl_cmd[2], int(spl_cmd[3])), conn_type=ConnType.TCP_CONN)
            elif spl_cmd[4] == "REV_SHELL":
                m.create_node(spl_cmd[1], (spl_cmd[2], int(spl_cmd[3])), conn_type=ConnType.REV_SHELL)
        elif spl_cmd[0] == 'status':
            node = m.get_node(spl_cmd[1])
            m.node_status(node)
        elif spl_cmd[0] == 'list':
            m.list_nodes()
        elif spl_cmd[0] == 'info':
            node = m.get_node(spl_cmd[1])
            m.node_info(node)
        elif spl_cmd[0] == 'shell':
            node = m.get_node(spl_cmd[1])
            m.shell(node, hist=True)
        elif spl_cmd[0] == "close":
            node = m.get_node(spl_cmd[1])
            m.close(node)
        elif spl_cmd[0] == "export":
            m.export_history("session_info.txt")
        elif spl_cmd[0] == 'clear':
            s('clear')
        elif spl_cmd[0] in ['quit', 'exit']:
            break
        else:
            print("Invalid command!")


def help():
    """Display possible commands to user
        connect "name" '127.0.0.1' 1234 ConnType.REV_SHELL
        connect "name" '65.123.3.1' 1337 ConnType.TCP_CONN

        list - list nodes

        status <node>   print node status
        info <node>     display info on a node
        shell <node> 
        help
    """
    pass

if __name__ == '__main__':
    main()

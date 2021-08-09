#!/usr/bin/env python3
import shutil
from c_color import *
from os import system as s
from c_manager import *
from sys import platform

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
        elif spl_cmd[0] == "help":
            aghelp()
        elif spl_cmd[0] == 'clear':
            clear()
        elif spl_cmd[0] in ['quit', 'exit']:
            break
        else:
            print("Invalid command!")


def aghelp():
    """Display possible commands to user
        connect "name" '127.0.0.1' 1234 ConnType.REV_SHELL
        connect "name" '65.123.3.1' 1337 ConnType.TCP_CONN

        list - list nodes

        status <node>   print node status
        info <node>     display info on a node
        shell <node> 
        help
    """
    print('''
    connect <name> <ip> <port> <connection_type> - Create a node for specific connectoin type.
        * Connection Types:
            TCP_CONN  -> Directly connect to remote shell.
            REV_SHELL -> Set up listener to recieve reverse shell connection.
            (i.e.) connect node_name 192.168.0.3 1337 TCP_CONN
                   connect node_name 0.0.0.0 1234 REV_SHELL
    
    list            - List All Nodes
    status <node>   - Get the status of a specific node (DEAD, LISTENING, CONNECTED)
    info <node>     - Get basic information of a given node connection. (Hostname, current user, os version)
    shell <node>    - Drop into a shell on the given node and run commands manually.
    help            - Display this help information.
    close <node>    - Close a connection on a given node.
    export          - Export a text file containing every command run, with its output.
    quit, exit      - Close automatic goggles and kill connections.
    ''')

def clear():
    if "win" in platform:
        s("cls")
    else:
        s("clear")

if __name__ == '__main__':
    main()

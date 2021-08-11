#!/usr/bin/env python3
# TODO: Make arg parsing easier and require less to type? Just make it better bruh
# TODO: USE CMD module to make user input more fun!
# TODO: Have configuration file that allows for nodes to be preconfigured.

import cmd
from src.c_color import *
from src.c_manager import *
from os import system as s
import shutil
from sys import platform
import threading

def main():

    columns = shutil.get_terminal_size().columns
    printc(f"{Color.PURPLE}automatic goggles{Color.END}", columns)
    printc(f"{Color.BLUE}chase opsahl{Color.END}", columns)
    print()
    menu()


def printc(string, size):
    print(string.center(size))

def menu():
    m = Manager()
    while True:
        try:
            cmd = input(f"[{Color.YELLOW}~{Color.END}] ")
        except KeyboardInterrupt:
            print("\nExiting...")
            return

        spl_cmd = cmd.split(' ')
        if spl_cmd[0] == 'connect':
            if spl_cmd[3] == "TCP_CONN":
                m.create_node((spl_cmd[1], int(spl_cmd[2])), conn_type=ConnType.TCP_CONN)
            elif spl_cmd[3] == "REV_SHELL":
                t = threading.Thread(target=m.create_node, args=((spl_cmd[1], int(spl_cmd[2])), ConnType.REV_SHELL), daemon=True)
                t.start()
        elif spl_cmd[0] == 'status':
            if len(spl_cmd) == 2:
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
            try:
                if spl_cmd[1] == '*':
                    m.close_all()
                else:
                    node = m.get_node(spl_cmd[1])
                    m.close(node)
            except IndexError:
                print(f"Ope: Syntax error!")
        elif spl_cmd[0] == "export":
            m.export_cmd_history("session_info.txt")
        elif spl_cmd[0] in ['rm']:
            try:
                if spl_cmd[1] == "*":
                    m.remove_all()
                else:
                    m.remove_node(m.get_node(spl_cmd[1]))
            except IndexError:
                print("Ope: Syntax error!")
        elif spl_cmd[0] == "help":
            aghelp()
        elif spl_cmd[0] == 'clear':
            clear()
        elif spl_cmd[0] in ['quit', 'exit']:
            break
        else:
            print("Invalid command!")


def aghelp():
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
    close <node>, * - Close a connection on a given node.
    export          - Export a text file containing every command run, with its output.
    rm <node>,*     - Delete/Remove node from list. 
    quit, exit      - Close automatic goggles and kill connections.
    ''')

def clear():
    if "win" in platform:
        s("cls")
    else:
        s("clear")

if __name__ == '__main__':
    main()

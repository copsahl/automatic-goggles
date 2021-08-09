#!/usr/bin/env python3
import shutil
from os import system as s
from c_manager import *

# TODO: Have configuration file that allows for nodes to be preconfigured. 
def main():


    '''
    columns = shutil.get_terminal_size().columns
    printc("automatic goggles", columns)
    printc("chase opsahl", columns)
    print()
    '''
    m = Manager()
    m.create_node("chase's_node", ("192.168.0.207", 1337))
    m.create_node("reverse", ("0.0.0.0", 1234), conn_type=ConnType.REV_SHELL)
    m.list_nodes()

    name = input("Which node would you like: ")
    node = m.get_node(name)
    m.shell(node)
    node.close()
    m.node_status(node)

def printc(string, size):
    print(string.center(size))

def menu():
    pass

def help():
    """Display possible commands to user"""
    pass

if __name__ == '__main__':
    main()

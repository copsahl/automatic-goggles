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
    
    m = Manager()
    while True:
        try:
            m.cmdloop()
        except KeyboardInterrupt:
            break

def printc(string, size):
    print(string.center(size))


if __name__ == '__main__':
    main()

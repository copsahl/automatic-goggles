#!/usr/bin/env python3
# TODO: Have configuration file that allows for nodes to be preconfigured.
import cmd
from src.c_color import *
from src.c_manager import *
from os import system as s
import shutil
from sys import platform

def main():

    columns = shutil.get_terminal_size().columns
    printc(f"{Color.PURPLE}automatic goggles{Color.END}", columns)
    printc(f"{Color.BLUE}by chase opsahl{Color.END}", columns)
    print()
    
    m = Manager()
    on = True
    while on:
        try:
            m.cmdloop()
        except KeyboardInterrupt:
            on = False

def printc(string, size):
    print(string.center(size))


if __name__ == '__main__':
    main()

#!/usr/bin/env python3

from sys import exit
from os import system
from sys import platform
from server import C2Server, Shell
from threading import Thread


def main():

    # Create server object & display banner
    cc = C2Server('127.0.0.1', 1337)
    cc.banner()

    # Main program loop
    while True:
        
        # Wait for user to enter a command
        cmd = terminal(cc)

        # If-else block to determine commands and run accordingly
        if cmd[0:3] == "sh ": 
            shellCommand(cmd) # Run local shell command
        elif cmd[0:7] == "attach ":
            currShell = cc.getShell(int(cmd[7:])) # Grab the shell object associated with a specific ID
            currShell.sendCmd() # Use the current shell object to run commands until you quit
        elif cmd[0:5] == "kill ":
            sessID = int(cmd[5:])   # Grab session ID from command
            try:
                cc.killConnection(sessID)   # Try to kill the session
            except AttributeError:
                print("Session hasn't started, cannot kill!")   # If you can't kill, give warning
        elif cmd[0:7] == "listen ":
            newShell = Shell(cmd[7:])   # Create a new shell object

            # Create a listening Thread set as a daemon so we can kill it easier
            listenThread = Thread(target = newShell.listenForConnection)
            listenThread.daemon = True
            listenThread.start()    # Start listening
            cc.addConnection(newShell)  # Add our new connection to the list
        elif cmd in ['sessions', 's']:
            cc.listSessions()   # List all of our current sessions
        elif cmd in ['clear', 'c']:
            clear()
        elif cmd in ['help', 'h']:
            cc.cmdHelp()    
        elif cmd in ['quit', 'q', 'exit', 'e']:
            print("\nQuitting...")
            exit(0)
        else:
            print("Unrecognized command!") 


def clear():
    # Clear the screen

    if("win" in platform):
        system('cls')
    else:
        system('clear')


def terminal(server):
    # Used to get user supplied commands

    try:
        cmd = input("[<\033[93m*\033[00m>] ".format(server.publicIP))
        return cmd
    except KeyboardInterrupt:
        return 'q'


def shellCommand(cmd):
    # Used to run local shell commands

    shCmd = cmd[3:]
    system(shCmd)


if __name__ == '__main__':
    clear()
    main()

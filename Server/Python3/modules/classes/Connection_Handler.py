import threading
import modules.classes.Server as Server
import modules.classes.Logger as Logger
import modules.classes.Watchdog as Watchdog
import socket
import random


class connHandler():
    # Get socket
    # If connection:
    #   Send welcome/plz wait for server
    #   Start new server thread
    #   Send port new thread is on
    #   Close connection
    def __init__(self, *args, **kwargs):
        threading.Thread.__init__(self)
        self.port = kwargs.get('port', 4200)
        self.host = kwargs.get('host', "127.0.0.1")
        self.welcome = kwargs.get(
            "welcome", "SEER Server\nMweya Ruider - 2019\n\n")

        # The maximum amount of threads to run
        # (equates to the maximum amount of simultaneous connections).
        # 0 <- No limit
        self.max_threads = kwargs.get("max_threads", 0)

        # Server threads
        self.servers = []
        # List of ports in use
        self.server_ports = []

        # Logging file
        self.log = Logger.LogFile()

    def getActiveServers(self):
        return self.servers

    def getLog(self):
        return self.log

    def __str__(self):
        return "Connection Handler\nPort:\t"+str(self.port)+"\nHost:\t"+str(self.host)+"\nMax threads:\t"+str(self.max_threads)

    def run(self):
        print(self.welcome)
        print(self)
        w = Watchdog.watchdog()
        w.start()
        w.updateServerList(self.servers)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.bind((self.host, self.port))
            s.listen(10)
            conn, addr = s.accept()
            with conn:
                #global info_log
                self.log.logInfo("Connection from " + str(addr))

                def createServerThread():
                    # Set up server for client to talk to
                    # Get random number for port
                    server_port = random.randint(1024, 65000)
                    # Make sure random number is not already in use
                    while server_port in self.server_ports:
                        server_port = random.randint(1024, 65000)
                    new_server = Server.server(port=server_port)
                    try:
                        new_server.start()
                        self.server_ports.append(server_port)
                        self.servers.append(new_server)
                        self.log.logInfo(
                            "Thread responsible for port "+str(server_port)+" started")
                        return server_port
                    except Exception as e:
                        #global error_log
                        self.log.logError(str(e))

                # Make sure we don't make too many threads
                if self.max_threads > 0:
                    if self.max_threads > len(self.servers) + 1:
                        # Looks ok, create thread
                        new_server_port = createServerThread()
                        # Reply to client with new server port
                        try:
                            message = "Server available at port: " + \
                                str(new_server_port)
                            message = bytes(message, "utf-8")
                            conn.sendall(message)
                            self.log.logInfo("Handoff to port " +
                                             str(new_server_port)+" completed")
                        except Exception as e:
                            self.log.logError(str(e))
                    else:
                        #global error_log
                        self.log.logError(
                            "Thread limit hit, cannot create new thread")
                elif self.max_threads == 0:
                    new_server_port = createServerThread()
                    # Reply to client with new server port
                    try:
                        message = "Server available at port: " + \
                            str(new_server_port)
                        message = bytes(message, "utf-8")
                        conn.sendall(message)
                        self.log.logInfo("Handoff to port " +
                                         str(new_server_port)+" completed")
                    except Exception as e:
                        self.log.logError(str(e))

                conn.close()

                # while True:
                #    data = conn.recv(1024)
                #    if not data:
                #        break
        except Exception as e:
            self.log.logError(str(e))

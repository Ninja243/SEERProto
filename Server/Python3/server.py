import subprocess
import socket
import threading
import random
import time
# Offload this work to separate process
import modules.HTML2JSON.Python3.h2j as HTML2JSON

# Lists to store error messages in case something goes wrong
info_log = []
warning_log = []
error_log = []


class server(threading.Thread):
    def __init__(self, *args, **kwargs):
        threading.Thread.__init__(self)
        # The port to listen on
        self.port = kwargs.get('port', 6969)
        # A welcome message that can be displayed to clients connecting
        self.welcome = kwargs.get(
            "welcome", "SEER Server\nMweya Ruider - 2019\n\n")
        # The host to run this on
        self.host = kwargs.get('host', "")

    def run(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((self.host, self.port))
        s.listen(1)
        s.accept()
        # Handle request, on close / end of transmission
        # kill thread and free resources

        print()


class watchdog(threading.Thread):
    def __init__(self, *args, **kwargs):
        threading.Thread.__init__(self)
        # In seconds
        self.sleepTime = 1

    def run(self):
        def sleep():
            print("Sleeping for "+self.sleepTime+" second(s)")
            time.sleep(self.sleepTime)
            printServerStatus()

        def printServerStatus():
            print("Server status: ")
            printErrors()

        def printErrors():
            #global error_log
            print("\tErrors:")
            i = 0
            for error in error_log:
                i = i+1
                print("\t\t" + str(i) + ": " + str(error))
            printWarnings()

        def printWarnings():
            #global warning_log
            print("\tWarnings:")
            i = 0
            for warning in warning_log:
                i = i + 1
                print("\t\t" + str(i) + ": " + str(warning))
            printNotifications()

        def printNotifications():
            #global info_log
            print("\tNotifications:")
            i = 0
            for notification in info_log:
                i = i + 1
                print("\t\t" + str(i) + ": " + str(notification))
            sleep()


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
        self.host = kwargs.get('host', "")
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

    def run(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((self.host, self.port))
        s.listen(10)
        conn, addr = s.accept()
        with conn:
            #global info_log
            info_log.append("Connection from " + str(addr))

            # Set up server for client to talk to
            # Get random number for port
            server_port = random.randint(1024, 65000)
            # Make sure random number is not already in use
            while server_port in self.server_ports:
                server_port = random.randint(1024, 65000)
            # Make sure we don't make too many threads
            if self.max_threads > 0:
                if self.max_threads > len(self.servers) + 1:
                    # Looks ok, create thread
                    new_server = server(port=server_port)
                    try:
                        new_server.start()
                        self.server_ports.append(server_port)
                        self.servers.append(new_server)
                    except Exception as e:
                        #global error_log
                        error_log.append(str(e))
                else:
                    #global error_log
                    error_log.append(
                        "Thread limit hit, cannot create new thread")

            while True:
                data = conn.recv(1024)
                if not data:
                    break


if __name__ == "__main__":

    pass

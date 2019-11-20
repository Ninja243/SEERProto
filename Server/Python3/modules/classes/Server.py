import socket
import threading
import modules.classes.Logger as Logger
import datetime


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
        # Potentially helpful information for if this dies
        self.log = Logger.LogFile()

    def getLogs(self):
        return self.log

    def run(self):
        self.log.logInfo("Server started")
        self.log.logInfo(self.getName()+"\nPort:\t"+str(self.port) +
                         "\nHost:\t"+self.host+"\nMOTD:\t"+self.welcome)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.bind((self.host, self.port))
            s.listen(1)
            conn, addr = s.accept()
            with conn:
                # Get command + path from client

                # Get file bundle in path

                # Compress bundle

                # Encrypt bundle
                # Return information
                data = "Welcome to SEER"
                data = bytes(data, "utf-8")
                conn.sendall(data)
                conn.close()
            s.close()
            self.log.logInfo("Thread responsible for port " +
                             str(self.port) + " shutting down")
            raise SystemExit
        except SystemExit:
            pass
        except Exception as e:
            self.log.logError(str(e))
            filename = self.getName+str(datetime.datetime.now())+"-crash.log"
            self.log.dumpLogsToFile(filename)
            s.close()
        # Handle request, on close / end of transmission
        # kill thread and free resources

import threading
import modules.classes.Logger as Logger
import time
import os
import sys


class watchdog(threading.Thread):
    def __init__(self, *args, **kwargs):
        threading.Thread.__init__(self)
        # In seconds
        self.sleepTime = 1
        self.log = Logger.LogFile()
        self.servers = []
        self.server_errors = Logger.LogFile()

    def updateServerList(self, servers):
        self.servers = servers

    def run(self):
        self.log.logInfo("Watchdog started")
        print("\nWatchdog shell:")
        while True:
            choice = input(" > ")
            if choice.startswith("help"):
                args = choice.split()
                if (len(args) > 1):
                    # Remove the "help" word
                    filename = str(args.pop(1))
                    directories = os.listdir(
                        "modules/helpfiles/")
                    if (filename+".txt" in directories):
                        print(open("modules/helpfiles/" + filename + ".txt").read())
                    else:
                        print("[!] Helpfile not found")
                else:
                    print(open("modules/helpfiles/this.txt", "r").read())
            elif choice.startswith("shutdown"):
                args = choice.split()
                if (len(args) == 1):
                    # sys.exit(os.EX_OK)           <- Doesn't work
                    print("Soft shutdown not implemented yet")
                elif len(args) > 1:
                    if (args[1] == "hard") or (args[1] == "-hard"):
                        os._exit(os.EX_OK)
            elif choice.startswith("list "):
                args = choice.split()
                if (len(args) < 1):
                    print("[!] You need to supply a thing to list")
                    print("    E.g. servers, clients")
                else:
                    if (args[1] == "servers"):
                        i = 0
                        for server in self.servers:
                            i = i+1
                            print("\t"+str(i)+": "+str(server))
            else:
                self.log.logWarning(
                    str(choice)+" has not been implemented yet")
            choice = ""
        # while True:
        #    print("Sleeping for "+str(self.sleepTime)+" second(s)")
        #    time.sleep(self.sleepTime)
        #    print("\n\nServer status: ")
        #    print("\tErrors:")
        #    i = 0
        #    for error in self.log.getErrorLogs():
        #        i = i+1
        #        print("\t\t" + str(i) + ": " + str(error))
        #    print("\tWarnings:")
        #    i = 0
        #    for warning in self.log.getWarningLogs():
        #        i = i + 1
        #        print("\t\t" + str(i) + ": " + str(warning))
        #    print("\tNotifications:")
        #    i = 0
        #    for notification in self.log.getInfoLogs():
        #        i = i + 1
        #        print("\t\t" + str(i) + ": " + str(notification))

import datetime


class LogFile():

    def __init__(self, *args, **kwargs):
        # Lists to store error messages in case something goes wrong
        self.log_name = kwargs.get("log_name", "Log File")
        self.info_log = []
        self.warning_log = []
        self.error_log = []

    def getInfoLogs(self):
        return self.info_log

    def getWarningLogs(self):
        return self.warning_log

    def getErrorLogs(self):
        return self.error_log

    def logError(self, error):
        self.error_log.append(str(error)+"\n@ "+str(datetime.datetime.now()))

    def logWarning(self, warning):
        self.warning_log.append(str(warning)+"\n@ " +
                                str(datetime.datetime.now()))

    def logInfo(self, info):
        self.info_log.append(str(info)+"\n@ "+str(datetime.datetime.now()))

    def dumpLogsToFile(self, filename="log-" + str(datetime.datetime.now()) + ".txt"):
        f = open(filename, "w")
        f.write(self.__str__)
        f.close()

    def __str__(self):
        out = self.log_name

        out = out+"\n\tErrors:"
        i = 0
        for error in self.error_log:
            i = i+1
            out = out + "\n\t\t" + str(i) + ": " + error

        out = out+"\n\tWarnings:"
        i = 0
        for warning in self.warning_log:
            i = i+1
            out = out + "\n\t\t" + str(i) + ": " + warning

        out = out+"\n\tNotifications:"
        i = 0
        for notification in self.info_log:
            i = i+1
            out = out + "\n\t\t" + str(i) + ": " + notification
        return out

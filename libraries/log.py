import sys, os, datetime, time


class LOG_CL:
    busyFlag = False

    def __init__(self):
        self.delete_log()
        self.delete_watchdog_log()

    def actualTime(self):
        return str(time.strftime("%H:%M"))

    def actualDate(self):
        return str(time.strftime("%d-%m-%Y"))

    def add_log(self, information):
        while self.busyFlag == True:
            time.sleep(0.001)
        self.busyFlag = True
        actFile = open('Desktop/Home/log.txt', 'a+')
        actFile.write(self.actualTime() + ' ' + information+'\n')
        actFile.close()
        self.busyFlag = False
        print(self.actualTime() + ' ' + information)

    def delete_log(self):
        while self.busyFlag == True:
            time.sleep(0.001)
        self.busyFlag = True
        actFile = open('Desktop/Home/log.txt', 'w')
        actFile.write(self.actualDate() + "  " + self.actualTime() + " LOG:\n")
        actFile.close()
        self.busyFlag = False

    def add_watchdog_log(self, information):
        while self.busyFlag == True:
            time.sleep(0.001)
        self.busyFlag = True
        actFile = open('Desktop/Home/watchdog_log.txt', 'a+')
        actFile.write(self.actualTime() + ' ' + information +'\n')
        actFile.close()
        self.busyFlag = False

    def delete_watchdog_log(self):
        while self.busyFlag == True:
            time.sleep(0.001)
        self.busyFlag = True
        actFile = open('Desktop/Home/watchdog_log.txt', 'w')
        actFile.write(self.actualDate() + "  " + self.actualTime() + " LOG:\n")
        actFile.close()
        self.busyFlag = False

    def add_stuff_log(self, information):
        while self.busyFlag == True:
            time.sleep(0.001)
        self.busyFlag = True
        actFile = open('Desktop/Home/stuff.txt', 'a+')
        actFile.write(self.actualTime() + ' ' + information +'\n')
        actFile.close()
        self.busyFlag = False

log = LOG_CL()
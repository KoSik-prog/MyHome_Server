import sys, os, datetime, time


class LOG_CL:
    busyFlag = False

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
        actFile.write(self.actualDate() + "  " + self.actualTime())
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
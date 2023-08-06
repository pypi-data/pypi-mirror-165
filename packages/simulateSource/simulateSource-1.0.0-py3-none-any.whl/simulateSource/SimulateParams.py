class SimulateParams():
    gain = 0
    utcTime = None
    enableLocalEph = False
    localEphFile = None
    simulateTimeList = [0 for _ in range(7)]
    def simulateTimetest(self, year,month,day,hour,minute,second):

        self.simulateTimeList[0] = (year >> 8) & 0xFF
        self.simulateTimeList[1] = year & 0xff
        self.simulateTimeList[2] = month
        self.simulateTimeList[3] = day
        self.simulateTimeList[4] = hour
        self.simulateTimeList[5] = minute
        self.simulateTimeList[6] = second
        # print(self.simulateTimeList)
        return self.simulateTimeList
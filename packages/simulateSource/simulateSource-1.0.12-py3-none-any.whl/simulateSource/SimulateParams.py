class SimulateParams:
    gain = 0
    utcTime = None
    enableLocalEph = False
    localEphFile = None
    simulateTimeList = [0 for _ in range(7)]
    def simulateTimetest(self, year, month, day, hour, minute, second):
        if month<=12 and day<=31 and hour<=24 and minute<=60 and second<=60:
            # 判断时间数据格式
            self.simulateTimeList[0] = (year >> 8) & 0xFF
            self.simulateTimeList[1] = year & 0xff
            self.simulateTimeList[2] = month
            self.simulateTimeList[3] = day
            self.simulateTimeList[4] = hour
            self.simulateTimeList[5] = minute
            self.simulateTimeList[6] = second
            return self.simulateTimeList
        else:
            print("时间数据格式错误，重新模拟")

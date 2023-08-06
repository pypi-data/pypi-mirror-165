from simulateSource.SimulateSource import SimulateSource
class SimulateBehaviour(SimulateSource.ISimulateSourceInterface):

    def __init__(self, com):
        self.com = com
        self.simulateSource = SimulateSource(self.com)
        self.simulateSource.register(self)


        traceSimulateParams = self.simulateSource.getTraceSimulateParams()
        traceSimulateParams.simulateDisplaySpeed = 45
        traceSimulateParams.singleGain = 0
        traceSimulateParams.fileName = "xmu_to_xmut.txt"
        # traceSimulateParams.fileName = "walk_route.txt"
        traceSimulateParams.simulateTime = traceSimulateParams.simulateTimetest(2022,12,1,16,30,10)
        self.simulateSource.readMessage(traceSimulateParams.fileName)
        self.simulateSource.setTraceSimulateParams(traceSimulateParams)
        self.simulateSource.startTraceModeSimulate()


        # singleSimulateParams = self.simulateSource.getSingleSimulateParams()
        # singleSimulateParams.longitude = 123.397128
        # singleSimulateParams.latitude = 59.916527
        # singleSimulateParams.altitude= 100
        # singleSimulateParams.singleGain= 1
        # singleSimulateParams.simulateTime =  singleSimulateParams.simulateTimetest(2022, 8, 1, 16, 30, 10)
        # self.simulateSource.setSingleSimulateParams(singleSimulateParams)
        # self.simulateSource.startSingleModeSimulate()






    def onSimulateState(self, simulateState):
        print("模拟状态simulateState: ", simulateState)


    def onSimulateMode(self, Mode):
        print("仿真模式SimulateMode: ", Mode)

    def onCurrentGian(self, gain):
        print("onCurrentGian: ", gain)


    def onListenSetSimulateTime(self, year, month, day, hour, minute):
        print("监听设置模拟时间onListenSetSimulateTime: ", year, month, day, hour, minute)


    def onListenSimulateTrackSpeed(self, speed):
        print("监听轨迹模拟速度onListenSimulateTrackSpeed: ", speed)


    def onEnableLocalEPH(self, enable):
        print("使能本地星历数据onEnableLocalEPH: ", enable)



    def onListenStartTrackSimulate(self, startTrackSimulate):
        print("开始轨迹模拟", startTrackSimulate)


    def onListenStopTrackSimulate(self, stopTrackSimulate):
        print("正在结束轨迹仿真", stopTrackSimulate)


    def onListenStartInitTackSimulate(self, maxValue):
        print("正在初始化轨迹模拟")

    def onListenCountInitTrackSimulate(self, countInitTrackSimulate):
        print("初始化轨迹模拟计数：%d" %countInitTrackSimulate)


    def onListenReInitTrackSimulate(self, state):
        print("正在重新初始化轨迹模拟", state)

    def onListenEndInitTrackSimulate(self, state):
        print("结束初始化", state)

    def onListenSendDoneTrackSimulate(self, state):
        print("完成轨迹发送", state)


    def onListenSendTrackTimeOut(self, state):
        print("轨迹数据发送超时", state)


    def onListenFailInitTrackSimulate(self, state):
        print("初始化失败", state)


    def onListenStartSingleSimulate(self, startSingleSimulate):
        print("单点仿真已开启：", startSingleSimulate)

    def onListenStopSingleSimulate(self, stopSingleSimulate):
        print("正在结束单点仿真", stopSingleSimulate)

    # def onListenStartInitSingleSimulate(self, title, maxValue):
    #     pass
    #
    # def onListenCountInitSingleSimulate(self, countInitSingleSimulate):
    #     pass
    #
    # def onListenReInitSingleSimulate(self, state):
    #     pass
    #
    # def onListenEndInitSingleSimulate(self, state):
    #     pass
    #
    # def onListenSendDoneSingleSimulate(self, state):
    #     pass
    #
    #
    # def onListenSendSingleTimeOut(self, state):
    #     pass
    #
    #
    # def onListenFailInitSingleSimulate(self, state):
    #     pass
if __name__ == "__main__":
    simulateBehaviour = SimulateBehaviour("COM24")

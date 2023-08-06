import queue
import struct
import threading
import time
from abc import ABCMeta, abstractmethod

import numpy as np
from simulateSource.ParsePacket import ParsePacket

from simulateSource.SingleSimulateParams import SingleSimulateParams
from simulateSource.TransmissionConstant import TransmissionConstant
from simulateSource.SerialCommunication import TransDevice
from simulateSource.Packet import Packet
from simulateSource.TraceSimulateParams import TraceSimulateParams

class SimulateSource(TransDevice.ITransDeviceInterface):
    traceMsgError = False
    reInitTrackSimulate = False
    failInitTrackSimulate = False
    countInitTrackSimulate = 0
    sendTrackTimeOut = False
    sendDoneTrackSimulate = False
    tensorList = []
    readList = queue.Queue()
    # readList = queue.Queue(maxsize=200)
    endInitTackSimulate = False
    startInitTackSimulate = False
    startTrackSimulate = False
    startInitSingleSimulate = False
    stopTrackSimulate = False
    stopSingleSimulate = False
    startSingleSimulate = False
    bluetoothBLEState = None
    enableLocalEPH = None
    simulateTrackSpeed = None
    simulateYear1 = None
    simulateYear2 = None
    simulateMonth = None
    simulateDay = None
    simulateHour = None
    simulateMinute = None
    simulateState = None
    gain = None
    ephTran = False
    cmdQueue = queue.Queue()
    heart = False
    tensorcheck = None
    tensor = None
    transDevice = None
    packet = None
    recvQueue = None
    simulateMode = None
    simulateBehaviour = None
    singleSimulateParams = None
    traceSimulateParams = None
    simulateSourceInterface = None
    class ISimulateSourceInterface(metaclass=ABCMeta):
        def __init__(self):
            pass

        @abstractmethod
        def onSimulateState(self , simulateState):
            pass

        @abstractmethod
        def onSimulateMode(self, Mode):
            pass

        @abstractmethod
        def onCurrentGian(self, gain):
            pass

        @abstractmethod
        def onListenSetSimulateTime(self , year , month , day , hour , minute):
            pass

        @abstractmethod
        def onListenSimulateTrackSpeed(self, speed):
            pass

        @abstractmethod
        def onEnableLocalEPH(self, enable):
            pass


        @abstractmethod
        def onListenStartTrackSimulate(self, startTrackSimulate):
            pass

        @abstractmethod
        def onListenStopTrackSimulate(self, stopTrackSimulate):
            pass

        @abstractmethod
        def onListenStartInitTackSimulate(self, maxValue):
            pass

        @abstractmethod
        def onListenCountInitTrackSimulate(self, countInitTrackSimulate):
            pass

        @abstractmethod
        def onListenReInitTrackSimulate(self, state):
            pass

        @abstractmethod
        def onListenEndInitTrackSimulate(self, state):
            pass

        @abstractmethod
        def onListenSendDoneTrackSimulate(self, state):
            pass

        @abstractmethod
        def onListenSendTrackTimeOut(self, state):
            pass

        @abstractmethod
        def onListenFailInitTrackSimulate(self, state):
            pass




        @abstractmethod
        def onListenStartSingleSimulate(self, startSingleSimulate):
            pass

        @abstractmethod
        def onListenStopSingleSimulate(self, stopSingleSimulate):
            pass

    def __init__(self, com):
        self.com = com
        self.recvPacketList = []
        self.list = []
        self.transDevice = TransDevice(self.com, 115200, 0.5)
        self.transDevice.register(self)
        self.transDevice.serialState()
        self.transDevice.start()
        self.packet = Packet()

        # self.packet.readMessage(fileName)
        self.recvQueue = self.transDevice.getRecvQueue()
        self.singleSimulateParams = SingleSimulateParams()
        self.traceSimulateParams = TraceSimulateParams()

        self.recvPacket = [0 for _ in range(20)]
        self.cmdPacket = [0 for _ in range(20)]
        self.threads = []
        t1 = threading.Thread(target=self.parsePacket)
        self.threads.append(t1)
        t2 = threading.Thread(target=self.tensorSend)
        self.threads.append(t2)
        # t3 = threading.Thread(target=self.heartCheck)
        # self.threads.append(t3)
        # t4 = threading.Thread(target=self._queryDeviceState)
        # self.threads.append(t4)
        for t in self.threads:
            t.start()



    def register(self, callback):
        try:
            if isinstance(callback, self.ISimulateSourceInterface):
                # 接口需要进行类型判断，是 ISimulateSourceInterface 类型才能进行注册
                self.simulateSourceInterface = callback
        except Exception:
            print("注册失败：接口类型错误")


    def onDeviceState(self, state):
        print("state: ", state)

    # 开始模拟
    def _startSimulate(self):
        msg = self.packet.getCmdTran(TransmissionConstant.START_SIMULATE, None)
        self.transDevice.sendMessage(msg)
        while True:
            time.sleep(0.2)
            self.cmdPacket = self.cmdQueue.get()
            if (self.cmdPacket[2] & 0xFF) == 0x01:
                if (self.cmdPacket[3] & 0xFF) == 0xFF:
                    print("开始命令帧响应错误！")
                    return
                if (self.recvPacket[3] & 0xFF) == 0x00:
                    print("开始命令帧响应正确！")
                    return


    def stopSimulate(self):
        self._stopSimulate()
    # 停止模拟
    def _stopSimulate(self):
        msg = self.packet.getCmdTran(TransmissionConstant.STOP_SIMULATE, None)
        self.transDevice.sendMessage(msg)
        while True:
            self.cmdPacket = self.cmdQueue.get()
            time.sleep(0.2)
            if (self.cmdPacket[2] & 0xFF) == 0x02:
                if (self.cmdPacket[3] & 0xFF) == 0xFF:
                    print("结束模拟命令帧响应错误！")
                    return
                if (self.cmdPacket[3] & 0xFF) == 0x00:
                    self.startSingleSimulate = False
                    print("结束模拟命令帧响应正确！")
                    return

    # 设置单点增益
    def setSignalGain(self, gainIndB):
        i = 0
        msg = self.packet.getCmdTran(TransmissionConstant.SET_OUTPUT_SIGNAL_GAIN, gainIndB)
        self.transDevice.sendMessage(msg)
        self.cmdPacket = self.cmdQueue.get()
        while True:
            i += 1
            time.sleep(0.1)
            if (self.cmdPacket[2] & 0xFF) == 0x10:
                print("收到信号增益命令")
                return
            if i >= 20:
                return

    # 设置模拟场景时刻
    # 仿真时刻用二进制表示，形式为YY/MM//DD/HH/MM/SS. 对应的字节数为：2/1/1/1/1/1， 共计7个字节。
    def setSimulateSceneTime(self, startTime):
        i = 0
        msg = self.packet.getCmdTran(TransmissionConstant.SET_SIMULATE_SCENE_TIME, startTime)
        self.transDevice.sendMessage(msg)
        while True:
            i += 1
            time.sleep(0.2)
            self.cmdPacket = self.cmdQueue.get()
            # 解析
            if (self.recvPacket[2] & 0xFF) == 0x11:
                print("收到设置仿真场景时刻命令")
                self.simulateYear1 = self.recvPacket[3]
                self.simulateYear2 = self.recvPacket[4]
                self.simulateMonth = self.recvPacket[5]
                self.simulateDay = self.recvPacket[6]
                self.simulateHour = self.recvPacket[7]
                self.simulateMinute = self.recvPacket[8]
                # 回调仿真场景时刻
                self.simulateYear = ("%d%d"%(self.simulateYear1, self.simulateYear2))
                if self.simulateSourceInterface:
                    self.simulateSourceInterface.onListenSetSimulateTime(self.simulateYear, self.simulateMonth,
                                                                         self.simulateDay, self.simulateHour,
                                                                         self.simulateMinute)
                return
            if i >= 20:
                print("超时退出")
                return

    # 设置使能静态场景
    # 使能静态仿真场景则最高字节为0x01. 默认使能。 （静态模式下仅需填充轨迹的第0个tensor的数值）
    def enableStaticScene(self, staticEnable):
        i = 0
        msg = self.packet.getCmdTran(TransmissionConstant.ENABLE_STATIC_SCENE, staticEnable)
        self.transDevice.sendMessage(msg)
        while True:
            i += 1
            time.sleep(0.2)
            self.cmdPacket = self.cmdQueue.get()
            if (self.recvPacket[2] & 0xFF) == 0x12:
                print("收到使能静态场景命令")

                return
            if i >= 20:
                print("超时退出")
                return

    # 使能本地星历数据
    # ephLocalEn = 0x01. 通知device 通过本地获取本地星历数据。 ephLocalEn = 0x00. 表示星历数据由app 获取。 默认本地获取。
    def enableLocalEPHData(self , ephLocalEn):
        i = 0
        msg = self.packet.getCmdTran(TransmissionConstant.ENABLE_LOCAL_EPH_DATA, ephLocalEn)
        self.transDevice.sendMessage(msg)
        while True:
            i += 1
            time.sleep(0.2)
            self.cmdPacket = self.cmdQueue.get()
            if (self.recvPacket[2] & 0xFF) == 0x13:
                print("收到使能本地星历数据命令")
                self.enableLocalEPH = self.recvPacket[3] & 0xFF
                if self.simulateSourceInterface:
                    self.simulateSourceInterface.onEnableLocalEPH(self.enableLocalEPH)
                return
            if i >= 20:
                print("超时退出")
                return

    # 设置模拟源演示速度
    # speed
    # 用4个字节的浮点数表示。 静态仿真的时候该数值为0.
    def _setSimulateSourceDisplaySpeed(self, speed):
        i = 0
        msg = self.packet.getCmdTran(TransmissionConstant.SET_SIMULATESOURCE_DISPLAY_SPEED, speed)
        self.transDevice.sendMessage(msg)
        while True:
            i += 1
            time.sleep(0.2)
            self.cmdPacket = self.cmdQueue.get()
            if (self.recvPacket[2] & 0xFF) == 0x14:
                self.simulateTrackSpeed = self.recvPacket[3:7]
                if self.simulateSourceInterface:
                    self.simulateSourceInterface.onListenSimulateTrackSpeed(self.simulateTrackSpeed)
                print("收到设置模拟源演示速度据命令")

                return
            if i >= 20:
                print("超时退出")
                return

    # 设置RF测试状态
    # setRF用1个字节表示。 默认为0. 0x01表示关闭射频； 0x02:表示输出单频点信号。
    def setRFTestState(self, setRF):
        i = 0
        msg = self.packet.getCmdTran(TransmissionConstant.SET_RF_TEST_STATE, setRF)
        self.transDevice.sendMessage(msg)
        while True:
            i += 1
            time.sleep(0.2)
            self.cmdPacket = self.cmdQueue.get()
            if (self.recvPacket[2] & 0xFF) == 0x15:
                print("收到设置RF测试状态命令")
                return
            if i >= 20:
                print("超时退出")
                return

    # device状态查询
    def _queryDeviceState(self):
        packet = Packet()
        while True:
            time.sleep(10)
            msg = packet.getCmdTran(TransmissionConstant.QUERY_DEVICE_STATE, None)
            self.transDevice.sendMessage(msg)
            self.cmdPacket = self.cmdQueue.get()
            self.gain = self.cmdPacket[5] & 0xFF
            if (self.cmdPacket[2] & 0xFF) == 0x20:
                print("收到查询Device状态命令")
                if ((self.cmdPacket[3] >> 4) & 0xf) == 0x00:
                    self.simulateState = 0x00
                    # 回调仿真状态
                    if self.simulateSourceInterface:
                        self.simulateSourceInterface.onSimulateState(self.simulateState)
                    print("device处于处于IDLE状态")
                elif ((self.cmdPacket[3] >> 4) & 0xf) == 0x01:
                    self.simulateState = 0x01
                    if self.simulateSourceInterface:
                        self.simulateSourceInterface.onSimulateState(self.simulateState)
                    print("device预加载完成")
                elif ((self.cmdPacket[3] >> 4) & 0xf) == 0x02:
                    self.simulateState = 0x02
                    if self.simulateSourceInterface:
                        self.simulateSourceInterface.onSimulateState(self.simulateState)
                    print("device停止处理中")
                    # 返回停止单点模拟
                    if ((self.cmdPacket[3] >> 3) & 0x01) == 0x1:
                        self.stopSingleSimulate = True
                        if self.simulateSourceInterface:
                            self.simulateSourceInterface.onListenStopSingleSimulate(self.stopSingleSimulate)
                    # 返回停止轨迹模拟
                    elif ((self.cmdPacket[3] >> 3) & 0x01) == 0x0:
                        self.stopTrackSimulate = True
                        if self.simulateSourceInterface:
                            self.simulateSourceInterface.onListenStopTrackSimulate(self.stopTrackSimulate)
                elif ((self.cmdPacket[3] >> 4) & 0xf) == 0x03:
                    self.simulateState = 0x03
                    if self.simulateSourceInterface:
                        self.simulateSourceInterface.onSimulateState(self.simulateState)
                    print("仿真程序运行中")
                    if ((self.cmdPacket[3] >> 3) & 0x01) == 0x1:
                        print("正在进行单点仿真")
                    elif ((self.cmdPacket[3] >> 3) & 0x01) == 0x0:
                        print("正在进行轨迹仿真")
                if ((self.cmdPacket[3] >> 3) & 0x01) == 0x1:
                    self.simulateMode = 0x01
                    if self.simulateSourceInterface:
                        self.simulateSourceInterface.onSimulateMode(self.simulateMode)
                    print("device处于使能静态仿真场景状态")
                elif ((self.cmdPacket[3] >> 3) & 0x01) == 0x0:
                    self.simulateMode = 0x00
                    if self.simulateSourceInterface:
                        self.simulateSourceInterface.onSimulateMode(self.simulateMode)
                    print("device处于动态仿真场景状态")
                if ((self.cmdPacket[3] >> 2) & 0x01) == 0x1:
                    self.enableLocalEPH = 0x01
                    if self.simulateSourceInterface:
                        self.simulateSourceInterface.onEnableLocalEPH(self.enableLocalEPH)
                    print("使能本地星历数据")
                elif ((self.cmdPacket[3] >> 2) & 0x01) == 0x0:
                    self.enableLocalEPH = 0x00
                    if self.simulateSourceInterface:
                        self.simulateSourceInterface.onEnableLocalEPH(self.enableLocalEPH)
                    print("使能APP星历数据")
                if (self.cmdPacket[5] & 0xFF) >= 0x80:
                    print("要重新设置当前仿真")
                self.gain = self.cmdPacket[5] & 0xFF
                self.setGain(self.gain)
                break

    def setGain(self, gain):
     if gain != self.gain:
         self.gain = gain
         if self.simulateSourceInterface:
             self.simulateSourceInterface.onCurrentGian(self.gain)
             print("当前增益为：", self.gain)

    # 响应device轨迹数据发送请求帧
    def responseDeviceTranceRequestFrame(self):
        msg = self.packet.getCmdTran(TransmissionConstant.RESPONSE_DEVICE_TRACE_REQUEST_FRAME, None)
        self.transDevice.sendMessage(msg)

    # 重置星历数据index值
    def resetEphTranIndex(self, index):
        i = 0
        msg = self.packet.getCmdTran(TransmissionConstant.RESET_EPHTRAN_INDEX, index)
        self.transDevice.sendMessage(msg)
        while True:
            i += 1
            time.sleep(0.2)
            self.cmdPacket = self.cmdQueue.get()
            if (self.recvPacket[2] & 0xFF) == 0x40:
                print("重置EphTran index命令")
                return
            if i >= 20:
                print("超时退出")
                return

    # 重置轨迹index值
    def resetTraceTran(self, index):
        i = 0
        msg = self.packet.getCmdTran(TransmissionConstant.RESET_TRACETRAN_INDEX, index)
        self.transDevice.sendMessage(msg)
        while True:
            i += 1
            time.sleep(0.2)
            self.cmdPacket = self.cmdQueue.get()
            if (self.recvPacket[2] & 0xFF) == 0x41:
                print("重置TraceTran index命令")
                return
            if i >= 20:
                print("超时退出")
                return

    def setSingleSimulateParams(self, singleSimulateParams):
        self.singleSimulateParams.longitude = singleSimulateParams.longitude
        self.singleSimulateParams.latitude = singleSimulateParams.latitude
        self.singleSimulateParams.altitude = singleSimulateParams.altitude
        self.singleSimulateParams.singleGain = singleSimulateParams.singleGain
        self.singleSimulateParams.simulateTime = singleSimulateParams.simulateTime


    def getSingleSimulateParams(self):
        return self.singleSimulateParams

    def startSingleModeSimulate(self):
        self._stopSimulate()
        # 读取参数并发送对应命令
        if self.traceMsgError:
            print("位置信息错误")
            return

        msg = self.packet.getTensor(0, self.singleSimulateParams.longitude,
                                     self.singleSimulateParams.latitude,
                                     self.singleSimulateParams.altitude)

        # 设置单点仿真模式 0x01
        # 正在初始化
        self.transDevice.sendMessage(msg)
        time.sleep(2)
        ENABLE_STATIC_payload = [TransmissionConstant.ENABLE_STATIC]
        self.enableStaticScene(ENABLE_STATIC_payload)
        singleGain = self.singleSimulateParams.singleGain
        self.setSignalGain([singleGain])
        self.setSimulateSceneTime(self.singleSimulateParams.simulateTime)
        self.startSingleSimulate = True
        self._startSimulate()
        if self.simulateSourceInterface:
            self.simulateSourceInterface.onListenStartSingleSimulate(self.startSingleSimulate)

    def setTraceSimulateParams(self, traceSimulateParams):
        self.traceSimulateParams.longitude = traceSimulateParams.longitude
        self.traceSimulateParams.latitude = traceSimulateParams.latitude
        self.traceSimulateParams.altitude = traceSimulateParams.altitude
        self.traceSimulateParams.simulateDisplaySpeed = traceSimulateParams.simulateDisplaySpeed
        self.traceSimulateParams.traceGain = traceSimulateParams.traceGain
        self.traceSimulateParams.simulateTime = traceSimulateParams.simulateTime
        self.traceSimulateParams.fileName = traceSimulateParams.fileName

    def getTraceSimulateParams(self):
        return self.traceSimulateParams

    def startTraceModeSimulate(self):
        self._stopSimulate()
        # 读取参数并发送对应命令
        self.enableStaticScene([0x00])
        traceGain = self.traceSimulateParams.traceGain
        self.setSignalGain(traceGain)
        self.setSimulateSceneTime(self.traceSimulateParams.simulateTime)
        simulateDisplaySpeed = self.traceSimulateParams.simulateDisplaySpeed
        self._setSimulateSourceDisplaySpeed([simulateDisplaySpeed])
        # 回调开始轨迹模拟初始化
        self.startInitTackSimulate = True
        if self.simulateSourceInterface:
            self.simulateSourceInterface.onListenStartInitTackSimulate(self.startInitTackSimulate)
        self.tensor = True
        i = 1
        # 等待首个300组数据发送成功
        while True:
            time.sleep(1)
            if i<3:
                if not self.tensor:
                    i += 1
                    print("i=%d" % i)
                    self.tensor = True

            elif self.tensor == False and i>=3:
                print("900组数据发送完成")
                # 回调结束轨迹仿真初始化
                self.endInitTackSimulate = True
                if self.simulateSourceInterface:
                    self.simulateSourceInterface.onListenEndInitTrackSimulate(self.endInitTackSimulate)
                # 回调开启仿真
                self._startSimulate()
                # t4 = threading.Thread(target=self._queryDeviceState)
                # t4.start()
                self.startTrackSimulate = True
                if self.simulateSourceInterface:
                    self.simulateSourceInterface.onListenStartTrackSimulate(self.startTrackSimulate)
                return
            else:
                # 回调初始化计数
                # self.countInitTrackSimulate += 1
                # if self.simulateSourceInterface:
                #     self.simulateSourceInterface.onListenCountInitTrackSimulate(self.countInitTrackSimulate)
                # 回调初始化超时失败
                if self.countInitTrackSimulate >= 100:
                    self.failInitTrackSimulate = True
                    if self.simulateSourceInterface:
                        self.simulateSourceInterface.onListenFailInitTrackSimulate(self.failInitTrackSimulate)
                    self.failInitTrackSimulate = False
                    self.countInitTrackSimulate = 0
                    self.listenReInitTrackSimulate()
                    return


    # 监听重新初始化状态
    def listenReInitTrackSimulate(self):
        # 回调重新初始化状态
        self.startTraceModeSimulate()
        self.reInitTrackSimulate = True
        if self.simulateSourceInterface:
            self.simulateSourceInterface.onListenReInitTrackSimulate(self.reInitTrackSimulate)
        self.reInitTrackSimulate = False

    # 星历数据发送
    def ephTranSend(self):
        while True:
            time.sleep(0.1)
            if self.ephTran:
                print("星历数据发送")
                self.packet.getEphTran(0, None)
                self.ephTran = False

    # 轨迹数据发送，循环一次300组
    def tensorSend(self):
        i = 0
        b = 0
        while True:
            i += 1
            time.sleep(0.1)
            if self.tensor:
                self.tensorcheck = True
                # print("轨迹数据发送")
                print("开始时间", time.strftime("%Y-%m-%d %H:%M:%S"))
                self.tensorCheck()
                b+=1
                print("总共发送数据:", b * 300)
                self.tensor = False
                i = 0
            else:
                # 队列判空操作
                if not self.readList.empty():
                    if i >=600:
                        # 回调发送超时
                        self.sendTrackTimeOut = True
                        if self.simulateSourceInterface:
                            self.simulateSourceInterface.onListenSendTrackTimeOut(self.sendTrackTimeOut)
                        i -= 600
                        self.sendTrackTimeOut = False
                else:
                    # 队列为空则回调数据发送完成
                    self.sendDoneTrackSimulate = True
                    if self.simulateSourceInterface:
                        self.simulateSourceInterface.onListenSendDoneTrackSimulate(self.sendDoneTrackSimulate)
                        return

    # 轨迹数据校验
    def tensorCheck(self):
        packet = Packet()
        i = 0
        b = 0
        c = 0
        while True:
            time.sleep(0.01)
            if self.tensorcheck:
                # 队列判空操作
                if not self.readList.empty():
                    self.tensorList = self.readList.get()
                    # print(float(self.tensorList[14:28]),
                    #             float(self.tensorList[:13]),
                    #             float(self.tensorList[29:35]))

                    self.traceSimulateParams.longitude = float(self.tensorList[14:28])
                    self.traceSimulateParams.latitude = float(self.tensorList[:13])
                    self.traceSimulateParams.altitude = float(self.tensorList[29:35])
                    # self.traceSimulateParams.longitude = 0.0
                    # self.traceSimulateParams.latitude = 0.0
                    # self.traceSimulateParams.altitude = 10
                    msg = packet.getTensor(c, self.traceSimulateParams.longitude,
                                                self.traceSimulateParams.latitude,
                                                self.traceSimulateParams.altitude)
                    self.transDevice.sendMessage(msg)
                    i += 1
                    c = i
                    self.tensorcheck = False
                    if i >= 300 :
                        print("完成时间",time.strftime("%Y-%m-%d %H:%M:%S"))
                        print("轨迹校验第 %d 次" % i)
                        return
                else:
                    self.tensorcheck = False
                    return
            # else:
            #     time.sleep(0.1)
            #     b += 1
            #     if b >= 100 :
            #         print("轨迹校验第 %d 次等待反馈超时" % i)
            #         # msg = self.packet.getTensor(i, self.traceSimulateParams.longitude,
            #         #                             self.traceSimulateParams.latitude,
            #         #                             self.traceSimulateParams.altitude)
            #         c=i-1
            #         self.transDevice.sendMessage(msg)
            #         # self.tensorcheck = True
            #         b = 0



    # 心跳帧校验
    def heartCheck(self):
        i = 0
        packet = Packet()
        while True:
            msg = packet.getheart()
            self.transDevice.sendMessage(msg)
            time.sleep(3.5)
            if self.heart:
                print("心跳帧正常")
                self.heart = False
            else:
                i += 1
                if i >= 2:
                    print("超时未收到心跳帧")
                    return

    def parsePacket(self):
        self.recvPacketList = b''
        parsePacketF = ParsePacket()
        while True:
            time.sleep(0.01)
            dataList = self.recvQueue.get()
            self.recvPacketList += dataList
            if len(self.recvPacketList) >= 20:
                self.recvPacket = self.recvPacketList[:20]
                self.recvPacketList = self.recvPacketList[20:]
                parsePacketF.addPacket(self.recvPacket)
                if parsePacketF.checksum() == False:
                    print("校验位出现错误")
                if parsePacketF.checkSynByte() == False:
                    print("字节位出错")
                if (self.recvPacket[1] & 0xFF) == 0xBB:
                    self.heart = True
                    print("心跳帧")
                elif (self.recvPacket[1] & 0xFF) == 0xFF:
                    if (self.recvPacket[2] & 0xFF) == 0x00:
                        print("校验位错误")
                elif (self.recvPacket[1] & 0xFF) == 0x01:
                    if (self.recvPacket[2] & 0xFF) == 0x00:
                        self.tensorcheck = True
                        # print("轨迹数据正确",self.recvPacket[3:18])
                        # respnseQueue.input({"tarce",})
                    if (self.recvPacket[2] & 0xFF) == 0xff:
                        self.tensorcheck = False
                        print("轨迹数据错误",self.recvPacket[3:18])
                elif (self.recvPacket[1] & 0xFF) == 0x02:
                    if (self.recvPacket[2] & 0xFF) == 0x00:
                        self.ephTran = True
                        print("星历数据正确，请进行下一次传输")
                    if (self.recvPacket[2] & 0xFF) == 0xFF:
                        print("星历数据错误")
                elif (self.recvPacket[1] & 0xFF) == 0x03:
                    self.cmdQueue.put(self.recvPacket)
                    print("收到命令帧响应")
                elif (self.recvPacket[1] & 0xFF) == 0xE0:
                    self.tensor = True
                    self.responseDeviceTranceRequestFrame()
                    print("执行下一次轨迹分发")
            else:
                continue
    def readMessage(self, fileName):
        try:
            # 读入文件
            self.file = open(fileName, 'r')
            print(fileName)
        except FileNotFoundError:
            print("文件名", fileName)
            print('File is not found')
        else:

            lines = self.file.readlines()
            for line in lines:

                # 原数据按行读取，将每行原元素按‘，’分隔成新元素
                a = line.split(",")
                x = str('%.10f' %(float(a[2])*0.01))
                y = str('%.10f' %(float(a[4])*0.01))
                z = a[9]
                # 写入发送队列
                self.readList.put(x + " " + y + " " + z)
                # while True:
                #     time.sleep(0.1)
                #     if self.readList.not_full:
                #         print("文件正在读取")
                #         self.readList.put(x +" "+ y +" "+ z)
                #         break
                #     else:
                #         print("文件读取队列已满")
                #         continue
        print("文件读取完成" , self.readList.qsize())
    # def readMessageThread(self):
    #     t5 = threading.Thread(target=self.readMessage(self.traceSimulateParams.fileName))
    #     t5.start()

if __name__ == "__main__":
    simulateSource = SimulateSource("COM24")
    # simulateSource.readMessage("walk_route1.txt")

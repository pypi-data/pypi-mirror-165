import queue
import struct
import threading
import time
from abc import ABCMeta, abstractmethod
import serial
from simulateSource.ExitThreadMsg import ExitThreadMsg

class TransDevice(object):
    stopThreadFlag = False

    SendList = queue.Queue()
    RecvList = queue.Queue()
    RecvDone = True
    SendDone = True
    callback = None
    state = Nonemetaclass=ABCMeta

    class ITransDeviceInterface(metaclass=ABCMeta):
        def __init__(self):
            pass

        @abstractmethod
        def onDeviceState(self, state):
            pass


    def __init__(self, com, bps, timeout):
        # 串口号
        self.serialPort = com
        # 波特率
        self.baudRate = bps
        # 超时溢出
        self.timeout = timeout
        self.ser = serial.Serial(self.serialPort , self.baudRate, timeout=self.timeout)
        # 输入输出缓存清零
        self.ser.flushOutput()
        self.ser.flushInput()
        # 打印参数设置
        print("参数设置：串口=%s ，波特率=%d" % (self.serialPort, self.baudRate))
        # 接收队列和发送队列
        self.threads = []
        self.state = 0x01
        # 串口状态判断
        if self.ser.isOpen():
            print("serial open success")

    def register(self, callback):
        self.transDeviceInterface = callback

    def serialState(self):
        if self.ser.isOpen():
            # print("serial open success")
            if self.transDeviceInterface:
                self.transDeviceInterface.onDeviceState(self.state)

    # 接收函数
    def recvMessageThread(self):
        # 循环将数据写入接收队列
        while not self.stopThreadFlag:
            # 读取串口数据
            bytes = self.ser.read_all()  # str
            # 数据为空循环等待
            if bytes == b'':
                continue
            self.RecvList.put(bytes)  # 如果没有数据就阻塞线程，直到有数据进来



    def sendMessage(self, list):
        self.SendList.put(list)
    #
    # 发送函数
    # def sendMessageThread(self):
    #     while self.SendDone:
    #         time.sleep(0.01)
    #         if not self.SendList.empty():
    #             list = self.SendList.get()
    #             # print("发送数据",list)
    #             byte= struct.pack('20B', *list)
    #             self.ser.write(byte)

    def sendMessageThread(self):
        while not self.stopThreadFlag:
            list = self.SendList.get()  # 如果没有数据就阻塞线程，直到有数据进来
            if isinstance(list, ExitThreadMsg):
                self.stopThreadFlag = True  # 退出线程
                continue
            byte = struct.pack('20B', *list)
            self.ser.write(byte)

    def getRecvQueue(self):
        return self.RecvList

    # 开启线程
    def start(self):
        # 接收线程
        t1 = threading.Thread(target=self.recvMessageThread)
        self.threads.append(t1)
        # 发送线程
        t2 = threading.Thread(target=self.sendMessageThread)
        self.threads.append(t2)
        # 开启线程
        for t in self.threads:
            t.start()         

    # 结束线程
    def close(self):
        self.SendList.put(ExitThreadMsg)
        self.RecvDone = False
        self.SendDone = False
        for t in self.threads:
            t.join()
        # 关闭串口
        self.ser.close()
        return self.RecvDone == False & self.SendDone == False

if __name__ == "__main__":
    test = TransDevice("COM24", 115200, 0.5)
    # test.ReadMessage('walk_route1.txt')
    test.start()
    # test.close()
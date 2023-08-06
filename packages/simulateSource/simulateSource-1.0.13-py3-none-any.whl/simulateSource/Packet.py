import queue
import time
import numpy as np
from simulateSource.SerialCommunication import TransDevice
from simulateSource.TransmissionConstant import TransmissionConstant


class Packet(object):

    # 封装包
    def __init__(self):
        #数据帧
        self.innerPacket = [0 for _ in range(20)]
        self.inner_payload = [0 for _ in range(17)]
        self.innerPacket[0] = 0x55

    def __setStreamType(self, StreamType):
        self.innerPacket[1] = StreamType

    def __setCommonPayload(self, Payload):
        i = 0
        while i < len(Payload):
            self.innerPacket[2 + i] = Payload[i]
            i += 1

    def __Checksum(self):
        #加入检验位
        self.innerPacket[19] = 0
        for i in range(0, 19):
            self.innerPacket[19] += self.innerPacket[i]
        self.innerPacket[19] = ~ self.innerPacket[19]
        self.innerPacket[19] = self.innerPacket[19] & 0xff
        # print(self.innerPacket)

    def getheart(self):
        self.__setStreamType(0xBB)
        for i in range(0, 17):
            self.inner_payload[i] = 0
        self.__setCommonPayload(self.inner_payload)
        self.__Checksum()
        # print(self.innerPacket)
        return self.innerPacket


    def getTensor(self, index, longitude, latitude, altitude):
        self.__setStreamType(0x01)
        for i in range(0, 17):
            self.inner_payload[i] = 0
        self.inner_payload[0] = ((index >> 8) & 0xff)
        self.inner_payload[1] = (index & 0xff)
        amp = 3054198960
        longitude *= amp
        latitude *= amp
        altitude *= 1000
        longitude_value = int(longitude)
        for i in range(0, 5):
            self.inner_payload[2 + 4 - i] = ((longitude_value >> 8 * i) & 0xff)
        latitude_value = int(latitude)
        for i in range(0, 5):
            self.inner_payload[7 + 4 - i] = ((latitude_value >> 8 * i) & 0xff)
        altitude_value = int(altitude)
        for i in range(0, 5):
            self.inner_payload[12 + 4 - i] = ((altitude_value >> 8 * i) & 0xff)
        self.__setCommonPayload(self.inner_payload)
        self.__Checksum()
        # print("轨迹数据打包成功")
        return self.innerPacket

    # 获取命令帧
    def getCmdTran(self, commandID, payload):
        for i in range(0, 17):
            self.inner_payload[i] = 0
        # print("cmd",self.inner_payload)
        self.__setStreamType(0x03)
        if commandID == TransmissionConstant.START_SIMULATE:
            self.inner_payload[0] = TransmissionConstant.START_SIMULATE
        elif commandID == TransmissionConstant.STOP_SIMULATE:
            self.inner_payload[0] = TransmissionConstant.STOP_SIMULATE
        elif commandID == TransmissionConstant.QUERY_DEVICE_STATE:
            self.inner_payload[0] = TransmissionConstant.QUERY_DEVICE_STATE
        elif commandID == TransmissionConstant.SET_SIMULATE_SCENE_TIME:
            self.inner_payload[0] = TransmissionConstant.SET_SIMULATE_SCENE_TIME
        elif commandID == TransmissionConstant.ENABLE_STATIC_SCENE:
            self.inner_payload[0] = TransmissionConstant.ENABLE_STATIC_SCENE
        elif commandID == TransmissionConstant.ENABLE_LOCAL_EPH_DATA:
            self.inner_payload[0] = TransmissionConstant.ENABLE_LOCAL_EPH_DATA
        elif commandID == TransmissionConstant.SET_OUTPUT_SIGNAL_GAIN:
            self.inner_payload[0] = TransmissionConstant.SET_OUTPUT_SIGNAL_GAIN
        elif commandID == TransmissionConstant.SET_RF_TEST_STATE:
            self.inner_payload[0] =TransmissionConstant.SET_RF_TEST_STATE
        elif commandID == TransmissionConstant.SET_SIMULATESOURCE_DISPLAY_SPEED:
            self.inner_payload[0] = TransmissionConstant.SET_SIMULATESOURCE_DISPLAY_SPEED
        if payload is not None and len(payload) <= 17:
            for i in range(len(payload)):
                self.inner_payload [i+1]= payload[i]
        self.__setCommonPayload(self.inner_payload)
        self.__Checksum()
        # print("打包命令帧",self.innerPacket)
        return self.innerPacket

    def getEphTran(self, index, payload):
        length = None
        self.__setStreamType(0x02)
        for i in range(0, 17):
            self.inner_payload[i] = 0
        self.inner_payload[0] = ((index >> 8) & 0xff)
        self.inner_payload[1] = (index & 0xff)
        if len(payload) > 15:
            length = 15
        else:
            length = len(payload)
        i = 0
        while i < length:
            self.inner_payload[2 + i] = payload[i]
            i += 1
        self.__setCommonPayload(self.inner_payload)
        self.__Checksum()
        return self.innerPacket

if __name__ == "__main__":
     transDevice = TransDevice("COM2", 9600, 0.5)
    # sendPacket = Packet()
    # transDevice.start()
    # sendPacket.getTensor(0)
    # packet = sendPacket.getheart()
    # packet = sendPacket.getTensor(0, 20, 30, 50)
    # packet = sendPacket.getCmdTran(BLETransmissionConstant.SET_SIMULATESOURCE_DISPLAY_SPEED,None)
    # transDevice.sendMessage(packet)


    # transDevice.close()
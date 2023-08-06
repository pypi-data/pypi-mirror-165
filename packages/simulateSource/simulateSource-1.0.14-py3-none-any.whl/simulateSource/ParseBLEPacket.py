#解析包
class ParseBLEPacket(object):

    def __init__(self):
        #instance fields found by Java to Python Converter:
        self.packet = [0 for _ in range(20)]


    #添加需要解析的包
    def addPacket(self, packet):
        self.packet = packet


    def checkSynByte(self):
        if (self.packet[0] & 0xFF) == 0x55:
            return True
        return False

    def checksum(self):
        check = 0
        for i in range(0, 19):
            check += self.packet[i]
        if (check & 0xFF) == 0xFF: #校验正确
            return True
        return False



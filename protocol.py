import serial

class ProtocolException(Exception):
    pass

class Protocol(object):
    def __init__(self):
        self.ser = serial.Serial('/dev/ttyACM0', 115200)

    def present(self):
        self.ser.write('\xF4')
        return self.ser.read()[0] == '\x01'

    def getTrip(self):
        self.ser.write('\xFB')
        data = self.ser.read(48)

        if data[0] != '\x00':
            raise ProtocolException('protocol error. is the computer switched on?')

        result = {}
        result["distance"] = self.decode_binary(data[1:7]) / 100.0
        result["average"]  = self.decode_binary(data[15:19]) / 100.0
        result["topspeed"] = self.decode_binary(data[20:24]) / 100.0
        result["elapsed"]  = self.decode_binary_time(data[8:14])
        return result

    def getTotal(self):
        self.ser.write('\xFD')

        # first 14 bytes are uknown
        self.ser.read(14)

        data = self.ser.read(85)

        if data[0] != '\x00':
            raise ProtocolExcption('protocol error. is the computer switched on?')
        
        result = {}
        result["distance"] = self.decode_binary(data[32:37])
        result["elapsed"]  = self.decode_binary_time(data[42:50])
        return result

    def decode_binary(self, data):
        if len(data) == 0: return 0
        return ord(data[-1]) + self.decode_binary(list(data[:-1])) * 10

    def decode_binary_time(self, data):
        seconds = self.decode_binary(data[-2:])
        minutes = self.decode_binary(data[-4:-2])
        hours = self.decode_binary(data[:-4])
        return seconds + minutes * 60 + hours * 3600


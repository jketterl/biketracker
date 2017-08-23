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
        return result

    def decode_binary(self, data):
        if len(data) == 0: return 0
        return ord(data[-1]) + self.decode_binary(list(data[:-1])) * 10

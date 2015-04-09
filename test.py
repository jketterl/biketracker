import serial, time

ser = serial.Serial('/dev/ttyACM0', 115200)

def decode(data):
    if (len(data) == 0): return 0
    return ord(data[-1]) + decode(list(data[:-1])) * 10

while True:
    ser.write('\xF4')
    if (ser.read()[0] == '\x01'):
        print("bike computer connected; reading trip data...")
        ser.write('\xFB')
        data = ser.read(48)
        if (data[0] != '\x00'):
            print('data failure. please retry.')
        else:
            print('trip distance: %.2f' % (decode(data[2:7]) / 100.0))
            print('average      : %.2f' % (decode(data[15:19]) / 100.0))
            print('top speed    : %.2f' % (decode(data[20:24]) / 100.0))
        print('completed.')
        time.sleep(59)
    time.sleep(1)

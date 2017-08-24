from influxdb import InfluxDBClient
from protocol import Protocol, ProtocolException

computer = Protocol()
influx = InfluxDBClient('172.30.0.183', 8086, 'graphite', 'graphite', 'biketracker')

while True:
    print("please insert computer to begin...")

    while not computer.present():
        pass

    try:
        print("computer inserted - downloading data...")
        trip = computer.getTrip()
        print(trip)

        print("sending to influxdb...")
        influx.write_points([{
            "measurement":"trip",
            "fields":trip
        }])

        print("all OK. please remove computer")
    except ProtocolException as e:
        print("protocol failure: {0}".format(e))

    while computer.present():
        pass

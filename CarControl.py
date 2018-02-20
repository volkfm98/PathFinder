import serial
import time

class CarControl:
    def __init__(self, device): #тут типо ардуинка подключается7
        self.arduino_device = device
        self.ser = serial.Serial(self.arduino_device, 9600)
        time.sleep(2)

    def move(self, direction, speed): #1==прямо 0==стоп -1== назад так что ли?
        self.ser.write(int(direction).to_bytes(1, 'big')) #
        self.ser.write(int(speed).to_bytes(1, 'big')) #от 0 до 255

    def turn(self, degree): #предельные значения какие??
        self.ser.write(int(3).to_bytes(1, 'big'))
        self.ser.write(int(degree).to_bytes(1, 'big'))

    def portDBG(self):
        print(self.ser.readline())

    def __del__(self):
        self.ser.close()
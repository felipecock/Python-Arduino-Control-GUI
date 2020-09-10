"""
Listen to serial, return most recent numeric values
Lots of help from here:
http://stackoverflow.com/questions/1093598/pyserial-how-to-read-last-line-sent-from-serial-device
"""
from threading import Thread
import time
import serial
import random

last_received = ''
def receiving(ser):
    global last_received
    buffer = ''
    while True:
        buffer = buffer + ser.read(ser.inWaiting())
        if '\n' in buffer:
            lines = buffer.split('\n') # Guaranteed to have at least 2 entries
            last_received = lines[-2]
            #If the Arduino sends lots of empty lines, you'll lose the
            #last filled line, so you could make the above statement conditional
            #like so: if lines[-2]: last_received = lines[-2]
            buffer = lines[-1]


class SerialData(object):
    def __init__(self, init=50, SysInput=bytearray()):
        try:
            self.ser = ser = serial.Serial(
                port='/dev/ttyACM0', #NUEVO Para sistemas Unix-Like
                #port='com4',  #Para sistemas no UNIX
                baudrate=9600,
                bytesize=serial.EIGHTBITS,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                timeout=0.01,
                xonxoff=0,
                rtscts=0,
                interCharTimeout=None
            )
        except serial.serialutil.SerialException:
            #no serial connection
            self.ser = None
        else:
			Thread(target=receiving, args=(self.ser,)).start()
        
    def next(self, emitting):
        if not self.ser:
            return [20.0 + random.random()*10 , 40.0 + random.random()*10 , 60.0 + random.random()*10 , 80.0 + random.random()*10] #return anything so we can test when Arduino isn't connected
        #return a float value or try a few times until we get one
        self.ser.write(chr(emitting)) #Nuevo [Envia un dato al Arduino]
        for i in range(5):
            raw_line = last_received
            ArduinoState = raw_line.split(';')
            try:
				ArduinoState[0] = float(ArduinoState[0])
				ArduinoState[1] = float(ArduinoState[1])
				ArduinoState[2] = float(ArduinoState[2])
				ArduinoState[3] = float(ArduinoState[3])
				return ArduinoState
            except ValueError:
                print 'Sin Datos',raw_line
                time.sleep(.005)
        return [0.0 , 0.0 , 0.0 , 0.0]
    def __del__(self):
        if self.ser:
            self.ser.close()

if __name__=='__main__':
    s = SerialData()
    for i in range(500):
        time.sleep(.15)
        print s.next(0)
    print ('Listo')       

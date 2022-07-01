import time
import board
import adafruit_dht
import psutil
from Light import Relay

# We first check if a libgpiod process is running. If yes, we kill it!
for proc in psutil.process_iter():
    if proc.name() == 'libgpiod_pulsein' or proc.name() == 'libgpiod_pulsei':
        proc.kill()

class Temp:
    dpin = board.D18
    def __init__(self, pin = dpin): #GPIO PIN
        self.pin = pin
        self.setup()
    def setup(self):
        self.sensor = adafruit_dht.DHT11(self.pin)
    def getTemp(self):
        self.temp = self.sensor.temperature
        return self.temp
    def getHumidity(self):
        self.humidity = self.sensor.humidity
        return self.humidity

if(__name__ == '__main__'):
    Temp_min = 25       #this is temperature maximum value for tent
    Temp_max = 27
    T = Temp(board.D18) # GPIO 18
    heater = Relay(24,0.1,0.1) #18 GPIO 24
    cooler = Relay(23,0.1,0.1) #16 GPIO 23
    while True:
        try:
            temp = T.getTemp()
            humidity = T.getHumidity()
            print("Temperature: {}*C   Humidity: {}% ".format(temp, humidity))
            if(temp < Temp_min):
                heater.turnOff()
            elif(temp <= Temp_max and temp >= Temp_min):
                cooler.turnOff()
                heater.turnOn()
                #print("Temperture is %d be Carefully" %T.temp)
            else:
                cooler.turnOn()
        except RuntimeError as error:
            print(error.args[0])
            #time.sleep(0.5)
            continue
        except Exception as error:
            T.sensor.exit()
            raise error
        #time.sleep(0.5)


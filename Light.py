import time
import RPi.GPIO as GPIO

class Relay:
    defaultPin = 16     # GPIO 23
    defaultDelay = 10   # Delay Time
    def __init__(self, pin = defaultPin, delayOn = defaultDelay, delayOff = defaultDelay):
        self.pin = pin
        self.delayOff = delayOff
        self.delayOn = delayOn
        self.setup()
        self.turnOff(False)
        
    def setup(self):
        GPIO.setup(self.pin, GPIO.OUT) # set relay in as output

    def turnOn(self, d = True):
        if(d): # if delay is Turned on
            time.sleep(self.delayOn)
        GPIO.output(self.pin, GPIO.LOW) # pass low to relay to turn it on

    def turnOff(self, d = True):
        if(d): # if delay is Turned on
            time.sleep(self.delayOff)
        GPIO.output(self.pin, GPIO.HIGH) # pass high to relay to turn it off 
        
    def Blink(self, d = True):
        self.turnOn(d)
        self.turnOff(d)
        
if __name__ == '__main__':
    try: #Catch when script is interrupted, cleanup correctly

        # Write Here Code For Setup (Run once at start)
        GPIO.setmode(GPIO.BOARD)
        #l = Relay(7,1,1)
        
        while True:
            # Write Here Code that will Repeated (Run Continuoslly)
            l = Relay(7,1,1)
            for i in range(3):
                print("led 1",i)
                l.Blink()
            l = Relay(11,1,1)
            for i in range(3):
                print("led 2",i)
                l.Blink()
            l = Relay(13,1,1)
            for i in range(3):
                print("led 3",i)
                l.Blink()
            l = Relay(15,1,1)
            for i in range(3):
                print("led 4",i)
                l.Blink()
            l = Relay(23,1,1)
            for i in range(3):
                print("led 5",i)
                l.Blink()
            l = Relay(27,1,1)
            for i in range(3):
                print("led 5",i)
                l.Blink()
    except KeyboardInterrupt:
        print("Program Closed By User")

    finally:
        GPIO.cleanup()    
    

import time
import RPi.GPIO as GPIO

class Ultra:
    dtrig = 16  # GPIO 16
    decho = 20  # GPIO 20
    def __init__(self, trig = dtrig, echo = decho):
        self.trig = trig
        self.echo = echo
        self.setup()
        
    def setup(self):
        GPIO.setup(self.trig, GPIO.OUT)
        GPIO.setup(self.echo, GPIO.IN)
    def sendEcho(self):
        GPIO.output(self.trig, True)
        time.sleep(0.00001)
        GPIO.output(self.trig, False)
    def calcTime(self):
        self. sendEcho()
        self.start = 0
        self.stop = 0 
        while GPIO.input(self.echo) == 0:
            self.start = time.time()
            #print("LOW")
        while GPIO.input(self.echo) == 1:
            self.stop = time.time()
            #print("HIGH")
        self.time = self.stop - self.start
        return self.time
    def calcDist(self):
        self.calcTime()
        self.dist = (self.calcTime() * 34300) / 2
        return self.dist

if __name__ == '__main__':
    try: #Catch when script is interrupted, cleanup correctly

        # Write Here Code For Setup (Run once at start)
        GPIO.setmode(GPIO.BCM)
        min_Dist = 20
        u = Ultra(10,9)
        #print("HI")
        while True:
            # Write Here Code that will Repeated (Run Continuoslly)
            print("Dist is = ",u.calcDist());
            '''
            if(u.calcDist() <= 20):
                print("Someone is closer")
            else:
                print("Noone close")
            '''
            time.sleep(0.01)
    except KeyboardInterrupt:
        print("Program Closed By User")

    finally:
        GPIO.cleanup()    
    


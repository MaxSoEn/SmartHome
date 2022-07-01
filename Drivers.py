import RPi.GPIO as GPIO          
from time import sleep #https://docs.python.org/fr/3/library/time.html
#Libraries
#https://circuitpython.readthedocs.io/projects/servokit/en/latest/
from adafruit_servokit import ServoKit


class l298:
    din1 = 6
    din2 = 13
    din3 = 19
    din4 = 26
    den1 = 5
    den2 = 21
    dspeed = 25
    direc = 1
    def __init__(self, motnum = 1, in1 = din1, in2 = din2, en1 = den1, in3 = din3, in4 = din4,  en2 = den2,):
        self.motor = [[in1, in2, en1, 25, 1], [0, 0, 0, 0, 0]]
        self.motnum = motnum
        if(self.motnum == 2):
            self.motor[1] = [in3, in4, en2, 25, 1]
        self.setup()
        
    def setup(self):
        GPIO.setup(self.motor[0][0],GPIO.OUT)
        GPIO.setup(self.motor[0][1],GPIO.OUT)
        GPIO.setup(self.motor[0][2],GPIO.OUT)
        GPIO.output(self.motor[0][1],GPIO.LOW)
        GPIO.output(self.motor[0][0],GPIO.LOW)
        self.p1 = GPIO.PWM(self.motor[0][2],1000)
        self.p1.start(self.motor[0][3])
        if(self.motnum == 2):
            GPIO.setup(self.motor[1][0],GPIO.OUT)
            GPIO.setup(self.motor[1][1],GPIO.OUT)
            GPIO.setup(self.motor[1][2],GPIO.OUT)
            GPIO.output(self.motor[1][1],GPIO.LOW)
            GPIO.output(self.motor[1][0],GPIO.LOW)
            self.p2 = GPIO.PWM(self.motor[1][2],1000)
            self.p2.start(self.motor[1][3])


    def stop(self, m = 0): # m = 0 for first motor 1 for second and 2 for both
        if(m == 0): # if delay is Turned on
            GPIO.output(self.motor[0][0], GPIO.LOW)
            GPIO.output(self.motor[0][1], GPIO.LOW)
        elif(m == 1 and self.motnum == 2):
            GPIO.output(self.motor[1][0], GPIO.LOW)
            GPIO.output(self.motor[1][1], GPIO.LOW)
        elif(m == 2 and self.motnum == 2):
            GPIO.output(self.motor[0][0], GPIO.LOW)
            GPIO.output(self.motor[0][1], GPIO.LOW)
            GPIO.output(self.motor[1][0], GPIO.LOW)
            GPIO.output(self.motor[1][1], GPIO.LOW)

    def forward(self, m = 0):# m = 0 for first motor 1 for second and 2 for both
        if(m == 0): 
            self.motor[0][4] = 1
            GPIO.output(self.motor[0][0], GPIO.HIGH)
            GPIO.output(self.motor[0][1], GPIO.LOW)
        elif(m == 1 and self.motnum == 2):
            self.motor[1][4] = 1
            GPIO.output(self.motor[1][0], GPIO.HIGH)
            GPIO.output(self.motor[1][1], GPIO.LOW)
        elif(m == 2 and self.motnum == 2):
            self.motor[0][4] = 1
            GPIO.output(self.motor[0][0], GPIO.HIGH)
            GPIO.output(self.motor[0][1], GPIO.LOW)
            self.motor[1][4] = 1
            GPIO.output(self.motor[1][0], GPIO.HIGH)
            GPIO.output(self.motor[1][1], GPIO.LOW)
        else:
            print("Error IN Setup")
    def backward(self, m = 0):# m = 0 for first motor 1 for second and 2 for both
        if(m == 0): 
            self.motor[0][4] = 0
            GPIO.output(self.motor[0][0], GPIO.LOW)
            GPIO.output(self.motor[0][1], GPIO.HIGH)
        elif(m == 1 and self.motnum == 2):
            self.motor[1][4] = 0
            GPIO.output(self.motor[1][0], GPIO.LOW)
            GPIO.output(self.motor[1][1], GPIO.HIGH)
        elif(m == 2 and self.motnum == 2):
            self.motor[0][4] = 0
            GPIO.output(self.motor[0][0], GPIO.LOW)
            GPIO.output(self.motor[0][1], GPIO.HIGH)
            self.motor[1][4] = 0
            GPIO.output(self.motor[1][0], GPIO.LOW)
            GPIO.output(self.motor[1][1], GPIO.HIGH)
        else:
            print("Error IN Setup")
    def run(self, m = 0):# m = 0 for first motor 1 for second and 2 for both
        if(m == 0):
            if(self.motor[0][4] == 1):
                self.forward(m)
            else:
                self.backward(m)
        elif(m == 1 and self.motnum == 2):
            if(self.motor[1][4] == 1):
                self.forward(m)
            else:
                self.backward(m)
        elif(m == 2 and self.motnum == 2):
            if(self.motor[0][4] == 1):
                self.forward(0)
            else:
                self.backward(0)
                
            if(self.motor[1][4] == 1):
                self.forward(1)
            else:
                self.backward(1)
        else:
            print("Error IN Setup")
    def changeSpeed(self, m = 0, speed = 25):# m = 0 for first motor 1 for second and 2 for both:
        if(m == 0):
            self.motor[0][3] = speed
            self.p1.ChangeDutyCycle(self.motor[0][3])
        elif(m == 1 and self.motnum == 2):
            self.motor[1][3] = speed
            self.p2.ChangeDutyCycle(self.motor[1][3])
        elif(m == 2 and self.motnum == 2):
            self.motor[0][3] = speed
            self.p1.ChangeDutyCycle(self.motor[0][3])
            self.motor[1][3] = speed
            self.p2.ChangeDutyCycle(self.motor[1][3])
        else:
            print("Error IN Setup")
    def CSpeed(self, m = 0, speed = 'l'):
        if(m == 0 or (m == 1 and self.motnum == 2) or (m == 2 and self.motnum == 2)):
            if(speed == 'l'):
                self.changeSpeed(m, 25)
            elif(speed == 'm'):
                self.changeSpeed(m, 50)
            elif(speed == 'h'):
                self.changeSpeed(m, 75)
            elif(speed == 'o'):
                self.changeSpeed(m, 100)
            else:
                print("Error Speed")
        else:
            print("Error IN Setup")
    def openWindow(self, m = 0, s = 57, d = 0.41):
        self.changeSpeed(m, s) #m.CSpeed(2,speed = 'h')
        self.forward(m)
        sleep(d)
        self.stop(m)
    def closeWindow(self, m = 0, s = 57, d = 0.41):
        self.changeSpeed(m, s) #m.CSpeed(2,speed = 'h')
        self.backward(m)
        sleep(d)
        self.stop(m)

class PCA:
    #Constants
    nbPCAServo = 16
    minIMP  = 500
    maxIMP  = 2500
    minANG  = 0
    maxANG  = 180
    # function init
    def __init__(self, nbServo = nbPCAServo, minI = minIMP, maxI = maxIMP, minA = minANG, maxA = maxANG):
        #Objects
        #self.minI = minI
        self.MIN_IMP = minI
        self.MAX_IMP = maxI
        self.MIN_ANG = minA
        self.MAX_ANG = maxA
        self.nbServo = nbServo
        self.isOpen = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.setup()

    def setup(self):
        self.p = ServoKit(channels=self.nbServo)
        for i in range(self.nbServo):
            self.p.servo[i].set_pulse_width_range(self.MIN_IMP , self.MAX_IMP)
        self.closeDoor(4) #close the front door

    def closeDoor(self,servoNum = 4, Force = 0):
        if(self.isOpen[servoNum] == 1 or Force == 1):
            for i in range(0,130,10):
                self.setServoAngle(servoNum,i)
                sleep(0.1)
            self.isOpen[servoNum] = 0

    def openDoor(self,servoNum = 4, Force = 0):
        if(self.isOpen[servoNum] == 0 or Force == 1):
            for i in range(120,-10, -10):
                self.setServoAngle(servoNum,i)
                sleep(0.1)
            self.isOpen[servoNum] = 1

    # function main 
    def main(self):
        self.pcaScenario();

    # function pcaScenario 
    def pcaScenario(self):
        #pass
        """Scenario to test servo"""
        for i in range(4,5): #range(self.nbServo):
            for j in range(self.MIN_ANG,self.MAX_ANG,20):
                print("Send angle {} to Servo {}".format(j,i))
                self.setServoAngle(i, j)
                sleep(0.1)
            for j in range(self.MAX_ANG,self.MIN_ANG,-20):
                print("Send angle {} to Servo {}".format(j,i))
                self.setServoAngle(i, j)
                sleep(0.1)
            self.setServoAngle(i, None) #disable channel
            sleep(1)
    def setServoAngle(self, servoNum = 0, angle = 90):
        self.p.servo[servoNum].angle = angle

if( __name__ == '__main__'):
    try: #Catch when script is interrupted, cleanup correctly
        
        # Write Here Code For Setup (Run once at start)
        GPIO.setmode(GPIO.BCM)
        m = l298(2, en1=5, in1=6, in2=13, in3=19, in4=26, en2=21)

        ''' for test Servos
        s = PCA(16)
        for j in range(0,5):
            #if(j != 2 and j != 3):
                if(j != 4):
                    for i in range(0,130,10):
                        print("Close Door",j)
                        s.setServoAngle(j,i) #main()
                        sleep(0.1)
                    sleep(3)
                else:
                    for i in range(120,-10,-10):
                        print("Open Door",j)
                        s.setServoAngle(j,i) #main()
                        sleep(0.1)
                    sleep(3)
        for j in range(0,5):
            #if(j != 2 and j != 3):
                if(j == 4):
                    for i in range(0,130,10):
                        print("Close Door",j)
                        s.setServoAngle(j,i) #main()
                        sleep(0.1)
                    sleep(3)
                else:
                    for i in range(120,-10,-10):
                        print("Open Door",j)
                        s.setServoAngle(j,i) #main()
                        sleep(0.1)
                    sleep(3)

        '''
        print("\n")
        print("The default speed & direction of motor is LOW & Forward.....")
        print("r-run s-stop f-forward b-backward l-low m-medium h-high e-exit")
        print("\n")    

        while(1):
        # Write Here Code that will Repeated (Run Continuoslly)
            x = input()
    
            if x=='r':
                print("run")
                if(m.motor[0][4] == 1):
                    print("forward1")
                    m.forward(2)
                    x='z'
                else:
                    print("backward1")
                    m.backward(2)
                    x='z'
                '''
                if(m.motor[1][4] == 1):
                    print("forward2")
                    m.forward(1)
                    x='z'
                else:
                    print("backward2")
                    m.backward(1)
                    x='z'
                '''
            elif x=='s':
                print("stop1")
                m.stop(2)
                x='z'

            elif x=='f':
                print("forward1")
                m.forward(2)
                x='z'

            elif x=='b':
                print("backward1")
                m.backward(2)
                x='z'

            elif x=='l':
                print("low")
                m.CSpeed(2,speed = x)
                x='z'

            elif x=='m':
                print("medium")
                m.CSpeed(2,speed = x)
                x='z'

            elif x=='h':
                print("high")
                m.CSpeed(2,speed = x)
                x='z'
            elif x=='o':
                print("max")
                m.CSpeed(2,speed = x)
                x='z'
            elif x =='q':
                m.openWindow(0, d=0.7)
                m.openWindow(1, d=0.46)
                x = 'z'
            elif x =='e':
                m.closeWindow(0, d=0.6)
                m.closeWindow(1, d=0.6)
                x = 'z'
            elif x=='e':
                print("GPIO Clean up")
                break
            else:
                print("<<<  wrong data  >>>")
                print("please enter the defined data to continue.....")

    except KeyboardInterrupt:
        print("Program Closed By User")

    finally:
        GPIO.cleanup()

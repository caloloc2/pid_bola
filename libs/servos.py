import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)

class Servos():

    def __init__(self, pin, frequency=50):
        self.__pin = pin
        self.__frequency = frequency
        self.__control = None
        #Initialize de servo
        self.__setup_servo()
    
    def __setup_servo(self):
        GPIO.setup(self.__pin, GPIO.OUT)
        self.__control = GPIO.PWM(self.__pin, self.__frequency)
        self.__control.start(0)
    
    def changeDuty(self, new_frequency):
        self.__control.ChangeDutyCycle(new_frequency)
    
    def stop_servo(self):
        self.__control.stop()
        # GPIO.cleanup()
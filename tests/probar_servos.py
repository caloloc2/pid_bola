import time
from libs.servos import Servos

servo1 = Servos(15)
servo2 = Servos(18)

procesa = True
tiempo = 0.2

while(procesa):
    try:
        servo1.changeDuty(5)
        servo2.changeDuty(6.5)
        time.sleep(tiempo)
        servo1.changeDuty(7.5)
        servo2.changeDuty(9.5)
        time.sleep(tiempo)
        servo1.changeDuty(9.5)
        servo2.changeDuty(12)
        time.sleep(tiempo)
        servo1.changeDuty(7.5)
        servo2.changeDuty(9.5)
        time.sleep(tiempo)
        servo1.changeDuty(5)
        servo2.changeDuty(7)
        time.sleep(tiempo)
        servo1.changeDuty(1)
        servo2.changeDuty(6.5)
        time.sleep(tiempo)
    except KeyboardInterrupt:
        procesa = False
        servo1.stop_servo()
        servo2.stop_servo()

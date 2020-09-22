import cv2, time
import numpy as np
from libs.camerastream import VideoStreaming
from libs.pid import PID
from libs.servos import Servos

class VideoCamera(object):

    def __init__(self, pidx, pidy, resolution=(320, 240), framerate=32):
        self.vs = VideoStreaming(resolution, framerate, brightness = 60, contrast= 50)
        self.vs.start()
        self.tau = 0.1
        self.control_x = PID(pidx[0], pidx[1], pidx[2], self.tau, 6.5, 12)
        self.control_y = PID(pidy[0], pidy[1], pidy[2], self.tau, 1, 9.5)
        self.servo1 = Servos(15)
        self.servo2 = Servos(18)
        self.muestreo = 0

    def get_frame(self):
        tiempo = time.time()
        frame = self.vs.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # apply a blur using the median filter
        img = cv2.medianBlur(gray, 5)

        # finds the circles in the grayscale image using the Hough transform
        circles = cv2.HoughCircles(image=img, method=cv2.HOUGH_GRADIENT, dp=0.9, minDist=2, param1=50, param2=30, minRadius=1, maxRadius=40)

        if circles is not None:
            circles = np.uint16(np.around(circles))
            for i in circles[0, :]:
                center = (i[0], i[1])

                # EJE X                
                servox = self.control_x.compute(154, i[0], self.muestreo)
                servox_m = self.control_x.map(servox, 6.5, 12, 12, 6.5)
                print(center, servox, servox_m)
                self.servo2.changeDuty(servox_m)

                # EJE Y                
                servoy = self.control_y.compute(114, i[1], self.muestreo)
                servoy_m = self.control_y.map(servoy, 1, 9.5, 9.5, 1)
                print(center, servoy, servoy_m)                
                self.servo1.changeDuty(servoy_m)
                
                # circle center
                cv2.circle(frame, center, 1, (0, 100, 100), 2)
                # circle outline
                radius = i[2]
                cv2.circle(frame, center, radius, (255, 0, 255), 2)

        ret, jpeg = cv2.imencode('.jpg', frame)
        self.muestreo = time.time() - tiempo
        
        return jpeg.tobytes()
    
    def cambiar_PID(self, pidx, pidy):
        self.control_x.set_gains(pidx[0], pidx[1], pidx[2], self.tau)
        self.control_y.set_gains(pidy[0], pidy[1], pidy[2], self.tau)
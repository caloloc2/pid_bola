import cv2, time
import numpy as np

class OpenCV:

    def image(x, y):
        x= int(x) + 250
        y= int(y) + 250
        img = np.ones((500,500,1),np.uint8)*0        
        cv2.circle(img, (x, y), 10, (255, 0, 0), -1)
        cv2.imwrite('image.png', img)        

    def analiza():        
        frame = cv2.imread('image.png')
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # apply a blur using the median filter
        img = cv2.medianBlur(gray, 5)        

        # finds the circles in the grayscale image using the Hough transform
        circles = cv2.HoughCircles(image=img, method=cv2.HOUGH_GRADIENT, dp=0.9, minDist=2, param1=10, param2=10, minRadius=1, maxRadius=15)

        center = (0, 0)
        if circles is not None:
            circles = np.uint16(np.around(circles))
            for i in circles[0, :]:
                center = (i[0], i[1])                 
        
        return center
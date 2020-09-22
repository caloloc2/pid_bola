from picamera.array import PiRGBArray
from picamera import PiCamera
from threading import Thread
import cv2, time

class VideoStreaming:

    def __init__(self, resolution=(320, 240), framerate=32, **kwargs):
        # inicializa la camara
        self.camera = PiCamera()

        # configura resolucion y framerate
        self.camera.resolution = resolution
        self.camera.framerate = framerate

        # configura parametros adicionales PiCamera
        for (arg, value) in kwargs.items():
            setattr(self.camera, arg, value)

        # inicia el streaming
        self.rawCapture = PiRGBArray(self.camera, size=resolution)
        self.stream = self.camera.capture_continuous(self.rawCapture, format="bgr", use_video_port=True)

        # inicializa frame
        self.frame = None
        self.stopped = False

        print("[INFO] - Iniciando camara")
        time.sleep(2.0)
        print("[INFO] - Camara iniciada")
    
    def start(self):
        t = Thread(target=self.update, args=())
        t.daemon = True
        t.start()
        return self
    
    def update(self):
        for f in self.stream:
            self.frame = f.array
            self.rawCapture.truncate(0)

            if self.stopped:
                self.stream.close()
                self.rawCapture.close()
                self.camera.close()
                return
    
    def read(self):
        return self.frame
    
    def __del__(self):
        self.stopped = True
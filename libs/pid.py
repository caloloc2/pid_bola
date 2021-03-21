import time
import matplotlib.pyplot as plt

class PID:

    # Inicializacion
    def __init__(self, Kp, Ki, Kd, tau, lim_min, lim_max):
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        self.tau = tau
        self.lim_min = lim_min
        self.lim_max = lim_max
        self.integrator = 0.0
        self.differentiator = 0.0
        self.prev_error = 0.0
        self.prev_measurement = 0.0
        
    def set_gains(self, Kp, Ki, Kd, tau):
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        self.tau = tau
        self.differentiator = 0
    
    def get_gains(self):
        return [self.Kp, self.Ki, self.Kd, self.tau]        
    
    def map(self, x, in_min, in_max, out_min, out_max):
        return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
    
    def set_limits(self, lim_min, lim_max):
        self.lim_min = lim_min
        self.lim_max = lim_max

    def compute(self, setpoint, measurement, T):
        # Error
        error = setpoint - measurement
        # Proporcional
        proportional = self.Kp * error
        # Integral
        self.integrator = self.integrator + 0.5 * self.Ki * T * (error + self.prev_error)
        # Limites de la integral
        limMinInt = 0
        limMaxInt = 0
        if (self.lim_max > proportional):
            limMaxInt = self.lim_max - proportional
        else:
            limMaxInt = 0
        
        if (limMinInt < proportional):
            limMinInt = self.lim_min -proportional
        else:
            limMinInt = 0
        # Limitar la integral
        if (self.integrator > limMaxInt):
            self.integrator = limMaxInt
        elif (self.integrator < limMinInt):
            self.integrator = limMinInt   
        # Derivativa con filtro
        self.differentiator = (2.0 * self.Kd * (measurement - self.prev_measurement) + (2.0 * self.tau - T) * self.differentiator) / (2.0 * self.tau + T)
        # Calcular salida del PID y limitar salida
        pid = proportional + self.integrator + self.differentiator
        if (pid > self.lim_max):
            pid = self.lim_max
        elif (pid < self.lim_min):
            pid = self.lim_min

        self.prev_error = error
        self.prev_measurement = measurement
            
        return pid
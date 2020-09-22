import os, json, threading, time, socket
from datetime import datetime

class Setup():

    def __init__(self, name_file="setup.conf", name_module = "control"):
        self._path= os.getcwd()+"/"
        self._file = name_file
        self._max_time_connection = 30   
        self._module = name_module
        self._data = None

        print("[INFO] Iniciando aplicacion.")
        time.sleep(1.5)
        self.__initialize()
    
    def set_path(self, new_path):
        self._path = new_path
    
    def get_path(self):
        return self._path
    
    def set_file(self, new_file):
        self._file = new_file
    
    def get_file(self):
        return self._file
    
    def set_max_time_connection(self, new_time):
        self._max_time_connection = new_time
    
    def get_max_time_connection(self):
        return self._max_time_connection
    
    def __get_init_conf(self):
        data = {}
        data[self._module] = []
        data[self._module].append({
            'kpx': 1,
            'kix': 0,
            'kdx': 0,
            'kpy': 1,
            'kiy': 0,
            'kdy': 0,
        })        
        return data
    
    def __get_conf_from_file(self):
        with open(self._path+self._file) as json_file:
            data = json.load(json_file)
            return data
    
    def __initialize(self):
        if (os.path.isfile(self._path+self._file)==False):
            print("[INFO] Iniciando valores por defecto.")
            self._data = self.__get_init_conf()
            with open(self._path+self._file, 'w') as outfile:
                json.dump(self._data, outfile)
        else:
            print("[INFO] Obteniendo valores de configuracion.")
            self._data = self.__get_conf_from_file()

    def __update_file(self):
        with open(self._path+self._file, 'w') as outfile:
                json.dump(self._data, outfile)

    def get_parameter(self, parameter):
        try:
            for p in self._data[self._module]:                
                return p[parameter]
        except:
            return None
    
    def set_parameter(self, parameter, value):
        ind=0
        for k in self._data[self._module]:
            ind += 1
        self._data[self._module][(ind-1)][parameter] = value        
        self.__update_file()   
            
    # funciones de control de placa raspberry

    def ip_address(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            return s.getsockname()[0]
            s.close()            
        except:
            return "127.0.0.1"
    
    def get_time(self):
        now = datetime.now() 
        return now.strftime("%d-%m-%Y %H:%M:%S")
        
    def temperature(self):
        try:
            tFile = open('/sys/class/thermal/thermal_zone0/temp')
            temp = float(tFile.read())
            temp = temp/1000
        except:
            temp = 100

        return temp

    def reboot(self, delay=5):
        try:
            print("[INFO] Reinicio en "+str(delay)+" segundos...")
            time.sleep(delay)
            os.system("sudo reboot")
        except Exception(e):
            print("[ERROR] "+str(e))
    
    def poweroff(self, delay=5):
        try:
            print("[INFO] Apagado en "+str(delay)+" segundos...")
            time.sleep(delay)
            os.system("sudo shutdown -h now")
        except Exception(e):
            print("[ERROR] "+str(e))
from flask import Flask, render_template, request, Response
from libs.setup import Setup
from libs.camera import VideoCamera
import time, json

config = Setup()
app = Flask(__name__)

pidx = [config.get_parameter("kpx"), config.get_parameter("kix"), config.get_parameter("kdx")]
pidy = [config.get_parameter("kpy"), config.get_parameter("kiy"), config.get_parameter("kdy")]

video_camara = VideoCamera(pidx, pidy)

@app.route('/')
def inicio():
    return render_template('index.html')

@app.route('/getData')
def getData():
    return json.dumps({'status':'OK', 'temperatura': config.temperature(), 'tiempo': config.get_time()});

@app.route('/getIP')
def getIP():
    return json.dumps({'status':'OK', 'ip_address': config.ip_address()});

@app.route('/getPIDs')
def getPIDs():
    return json.dumps({'status':'OK', 'pidx': pidx, 'pidy': pidy});

@app.route('/setCx', methods=['POST'])
def setCx():
    pidx[0] =float(request.form['kp'])
    pidx[1] =float(request.form['ki'])
    pidx[2] =float(request.form['kd'])
    # Guarda la configuracion
    config.set_parameter("kpx", pidx[0])
    config.set_parameter("kix", pidx[1])
    config.set_parameter("kdx", pidx[2])

    video_camara.cambiar_PID(pidx, pidy)
    print("[INFO] Parametros PID Eje X asignados")

    return json.dumps({'status':'OK'});

@app.route('/setCy', methods=['POST'])
def setCy():
    pidy[0] =float(request.form['kp'])
    pidy[1] =float(request.form['ki'])
    pidy[2] =float(request.form['kd'])
    # Guarda la configuracion
    config.set_parameter("kpy", pidy[0])
    config.set_parameter("kiy", pidy[1])
    config.set_parameter("kdy", pidy[2])

    video_camara.cambiar_PID(pidx, pidy)
    print("[INFO] Parametros PID Eje Y asignados")
    
    return json.dumps({'status':'OK'});

@app.route('/bootRasp', methods=['POST'])
def bootRasp(): 
    if (str(request.form['opcion'])=='reboot'):
        config.reboot()
    elif (str(request.form['opcion'])=='poweroff'):
        config.poweroff()    

    return json.dumps({'status':'OK'});

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(video_camara),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":    
    app.run(host='0.0.0.0', debug=False)
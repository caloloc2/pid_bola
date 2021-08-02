import time, json, math, threading, random
from flask import Flask, render_template, request, Response
from libs.pid import PID
from libs.pso import PSO
from libs.opencv import OpenCV

app = Flask(__name__)

def randomicos():
    return [math.floor(random.random()*250), math.floor(random.random()*250)]

def definir_funcion(O):
    x = O[0]
    y = O[1]
    nonlinear_constraint = (x - 1) ** 3 - y + 1
    linear_constraint = x + y - 2
    if nonlinear_constraint > 0:
        penalty1 = 1
    else:
        penalty1 = 0
 
    if linear_constraint > 0:
        penalty2 = 1
    else:
        penalty2 = 0
 
    z = (1 - x) ** 2 + 100 * (y - x ** 2) ** 2 + penalty1 + penalty2    
    return z

set_point = [250, 250] # posicion central en canvas x, y (width 500, height 500)
position = randomicos()

pidx = [0, 0, 0] # pid para control en el eje x
pidy = [0, 0, 0] # pid para control en el eje y

valoresx = []
valoresy = []

control_xa = PID(pidx[0], pidx[1], pidx[2], 0.1, 0, 250)
control_xb = PID(pidx[0], pidx[1], pidx[2], 0.1, -250, 0)
control_ya = PID(pidy[0], pidy[1], pidy[2], 0.1, 0, 250)
control_yb = PID(pidy[0], pidy[1], pidy[2], 0.1, -250, 0)

calcular = 0

canvas = OpenCV

@app.route('/')
def inicio():
    return render_template('index.html')

@app.route('/reset')
def reset():
    global position
    global pidx 
    global pidy 
    global calcular
    global valoresx
    global valoresy

    position = randomicos()

    pidx = [0, 0, 0] # pid para control en el eje x
    pidy = [0, 0, 0] # pid para control en el eje y 
    valoresx = []
    valoresy = []   
    calcular = 0

    return json.dumps({'status':'OK'})

@app.route('/setPos', methods=['POST'])
def setPos():
    global valoresy
    global valoresx
    global calcular

    position[0] = float(request.form['X'])
    position[1] = float(request.form['Y'])
    valoresx = []
    valoresy = []
    calcular = 0

    print("[INFO] Posicion ("+str(position[0])+", "+str(position[1])+") modificada por usuario")
    return json.dumps({'status':'OK'})

@app.route('/setPID', methods=['POST'])
def setPID():
    global control_xa
    global control_xb
    global control_ya
    global control_yb
    global valoresx
    global valoresy
    global calcular

    pidx[0] = float(request.form['kpx'])
    pidx[1] = float(request.form['kix'])
    pidx[2] = float(request.form['kdx'])

    pidy[0] = float(request.form['kpy'])
    pidy[1] = float(request.form['kiy'])
    pidy[2] = float(request.form['kdy'])

    control_xa.set_gains(pidx[0], pidx[1], pidx[2], 0.1)    
    control_xb.set_gains(pidx[0], pidx[1], pidx[2], 0.1)    
    control_ya.set_gains(pidy[0], pidy[1], pidy[2], 0.1)
    control_yb.set_gains(pidy[0], pidy[1], pidy[2], 0.1)

    valoresx = []
    valoresy = []

    calcular = 1

    print("[INFO] PID modificada por usuario")
    return json.dumps({'status':'OK'})

@app.route('/setPSO', methods=['POST'])
def setPSO():
    global control_xa
    global control_xb
    global control_ya
    global control_yb    
    global valoresx
    global valoresy

    pidx[0] = abs(PSO(definir_funcion, [(-1, 1), (0.5, 1)], 12, 100, [0.2, 1, 2]).evaluar()[0])
    pidx[1] = 0
    pidx[2] = abs(PSO(definir_funcion, [(-1, 1), (-0.01, 0.0001)], 12, 100, [0.5, 1, 2]).evaluar()[0])

    pidy[0] = abs(PSO(definir_funcion, [(-1, 1), (0.3, 1)], 12, 100, [0.12, 1, 2]).evaluar()[0])
    pidy[1] = 0
    pidy[2] = abs(PSO(definir_funcion, [(-1, 1), (-0.01, 0.00001)], 12, 100, [0.5, 1, 2]).evaluar()[0])

    control_xa.set_gains(pidx[0], pidx[1], pidx[2], 0.1)    
    control_xb.set_gains(pidx[0], pidx[1], pidx[2], 0.1)    
    control_ya.set_gains(pidy[0], pidy[1], pidy[2], 0.1)
    control_yb.set_gains(pidy[0], pidy[1], pidy[2], 0.1)

    valoresx = []
    valoresy = []

    print("[INFO] PSO calculando valores...")
    return json.dumps({'pidx' : pidx, 'pidy' : pidy, 'status':'OK'})

@app.route('/getPos')
def getPos():
    global position 
    global valoresx
    global valoresy

    datosx = "" #'-'.join(str(valoresx))
    for x in valoresx:
        valor = str(x)
        # if (x>set_point[0]):
        #     valor = str((x - 250))
        datosx += valor + "#"

    datosy = "" #'-'.join(str(valoresx))
    for y in valoresy:
        valor = str(y)
        # if (y>set_point[1]):
        #     valor = str((y - 250))
        datosy += valor + "#"
    return json.dumps({'position' : position, 'valoresx': datosx, 'valoresy': datosy, 'status':'OK'})

def control():
    global control_xa
    global control_xb
    global control_ya
    global control_yb
    global position
    global set_point
    global image
    global valoresx
    global valoresy
        
    muestreo = 0

    while (True):
        if (calcular == 1):
            tiempo = time.time()
            canvas.image(position[0], position[1])
            posx, posy = canvas.analiza()
            # print(posx, posy)
            valoresx.append(posx)
            valoresy.append(posy)
            print(valoresx, valoresy)

            if ((posx != 0) and (posy != 0)):
                error_xa = control_xa.compute(set_point[0], posx, muestreo)
                error_xb = control_xb.compute(set_point[0], posx, muestreo)

                error_ya = control_ya.compute(set_point[1], posy, muestreo)
                error_yb = control_yb.compute(set_point[1], posy, muestreo)

                position[0] += error_xa
                position[0] += error_xb
                position[1] += error_ya
                position[1] += error_yb
            else:
                position = randomicos()
            muestreo = time.time() - tiempo
        
        time.sleep(0.5)

resp = threading.Thread(target = control)
resp.daemon = True
resp.start()

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=False)
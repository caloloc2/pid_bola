var canvas = document.getElementById("lienzo");
if (canvas && canvas.getContext) {
    var ctx = canvas.getContext("2d");
    if (ctx) {
        var arrastrar = false;
        var X = 0;
        var Y = 0;
        const r = 10;

        function bola(X, Y) {
            ctx.clearRect(0, 0, canvas.width, canvas.height);

            ctx.setLineDash([5, 3]);/*dashes are 5px and spaces are 3px*/
            ctx.strokeStyle = "#444";
            ctx.lineWidth = 1;
            ctx.beginPath();
            ctx.moveTo(0, 250);
            ctx.lineTo(500, 250);
            ctx.stroke();

            ctx.beginPath();
            ctx.moveTo(250, 0);
            ctx.lineTo(250, 500);
            ctx.stroke();

            ctx.beginPath();
            ctx.strokeStyle = "#006400";
            ctx.fillStyle = "#6ab150";
            ctx.lineWidth = 2;
            ctx.arc((X + 250), (Y + 250), r, 0, 2 * Math.PI, false);
            ctx.fill();
            ctx.stroke();
            ctx.closePath();
        }

        function oMousePos(canvas, evt) {
            var rect = canvas.getBoundingClientRect();
            return { // devuelve un objeto
                x: Math.round(evt.clientX - rect.left),
                y: Math.round(evt.clientY - rect.top)
            };
        }

        canvas.addEventListener("mousedown", function (evt) {
            var mousePos = oMousePos(canvas, evt);

            bola(X, Y);
            if (ctx.isPointInPath(mousePos.x, mousePos.y)) {
                arrastrar = true;
                clearInterval(reload_pos)
            }
        }, false);

        canvas.addEventListener("mousemove", function (evt) {
            var mousePos = oMousePos(canvas, evt);

            if (arrastrar) {
                ctx.clearRect(0, 0, canvas.width, canvas.height);
                X = mousePos.x - 250,
                    Y = mousePos.y - 250

                bola(X, Y);
            }
        }, false);

        canvas.addEventListener("mouseup", function (evt) {
            arrastrar = false;
            setPos(X, Y)
            Actualizar_Posicion()
        }, false);

        /// envio y actualizacion de posicion de la bola

        var reload_pos = null;

        function Actualizar_Posicion() {
            reload_pos = setInterval(() => {
                getPos()                
            }, 500);
        }

        function getPos() {
            $.ajax({
                url: '/getPos',
                success: function (response) {

                    var respuesta = JSON.parse(response)
                    // console.log(respuesta);
                    if (respuesta.status == "OK") {
                        X = parseFloat(respuesta.position[0])
                        Y = parseFloat(respuesta.position[1])

                        bola(X, Y);
                    }
                },
                error: function (error) {
                    console.log(error);
                }
            });
        }

        function setPos(X, Y) {
            var position = { X, Y }
            $.ajax({
                url: '/setPos',
                data: position,
                type: 'POST',
                success: function (response) {
                    console.log(response);
                },
                error: function (error) {
                    console.log(error);
                }
            });
        }

        function setPID() {
            var pid = {
                kpx: document.getElementById("kpx").value,
                kix: document.getElementById("kix").value,
                kdx: document.getElementById("kdx").value,
                kpy: document.getElementById("kpy").value,
                kiy: document.getElementById("kiy").value,
                kdy: document.getElementById("kdy").value,
            }
            $.ajax({
                url: '/setPID',
                data: pid,
                type: 'POST',
                success: function (response) {
                    console.log(response);
                },
                error: function (error) {
                    console.log(error);
                }
            });
        }

        Actualizar_Posicion()

        $("#formulario_x").submit(e => {
            e.preventDefault()
            setPID()
        })

        $("#formulario_y").submit(e => {
            e.preventDefault()
            setPID()
        })

        function PSO() {
            $.ajax({
                url: '/setPSO',
                data: {},
                type: 'POST',
                success: function (response) {
                    // console.log(response);
                    var respuesta = JSON.parse(response)

                    if (respuesta.status == "OK") {
                        var pidx = respuesta.pidx
                        var pidy = respuesta.pidy
                        document.getElementById("kpx").value = pidx[0]
                        document.getElementById("kix").value = pidx[1]
                        document.getElementById("kdx").value = pidx[2]
                        document.getElementById("kpy").value = pidy[0]
                        document.getElementById("kiy").value = pidy[1]
                        document.getElementById("kdy").value = pidy[2]
                    }
                },
                error: function (error) {
                    console.log(error);
                }
            });
        }
    }
}


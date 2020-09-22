console.log("Server started");

$(document).ready(function(){
    Direccion_IP()
    setInterval(() => {
        Lectura()
    }, 1000);
    setInterval(() => {
        Direccion_IP()
    }, 1000 * 60);    
    getPids();
})

function Raspberry(opcion){
    $.ajax({
        url: '/bootRasp',
        data: {
            opcion
        },
        type: 'POST',
        success: function(response) {
            console.log(response);
        },
        error: function(error) {
            console.log(error);
        }
    });
}

function Lectura(){    
    $.ajax({
        url: '/getData',        
        success: function(response) {            
            const datos = JSON.parse(response);            
            $("#temp").html(parseFloat(datos.temperatura).toFixed(1));
            $("#tiempo").html(datos.tiempo);
        },
        error: function(error) {
            console.log(error);
        }
    });
}

function Direccion_IP(){    
    $.ajax({
        url: '/getIP',        
        success: function(response) {            
            const datos = JSON.parse(response);            
            $("#ip_address").html(datos.ip_address);            
        },
        error: function(error) {
            console.log(error);
        }
    });
}

function getPids(){
    $.ajax({
        url: '/getPIDs',        
        success: function(response) {            
            const datos = JSON.parse(response);            
            document.getElementById("kpx").value = parseFloat(datos.pidx[0]).toFixed(3);
            document.getElementById("kix").value = parseFloat(datos.pidx[1]).toFixed(3);
            document.getElementById("kdx").value = parseFloat(datos.pidx[2]).toFixed(3);

            document.getElementById("kpy").value = parseFloat(datos.pidy[0]).toFixed(3);
            document.getElementById("kiy").value = parseFloat(datos.pidy[1]).toFixed(3);
            document.getElementById("kdy").value = parseFloat(datos.pidy[2]).toFixed(3);
        },
        error: function(error) {
            console.log(error);
        }
    });
}

$("#formulario_x").submit((e) => {
    e.preventDefault();

    var campos = {
        kp: document.getElementById("kpx").value,
        ki: document.getElementById("kix").value,
        kd: document.getElementById("kdx").value,
    }
    console.log(campos);
    $.ajax({
        url: '/setCx',
        data: campos,
        type: 'POST',
        success: function(response) {
            console.log(response);
            getPids();
        },
        error: function(error) {
            console.log(error);
        }
    });
})

$("#formulario_y").submit((e) => {
    e.preventDefault();

    var campos = {
        kp: document.getElementById("kpy").value,
        ki: document.getElementById("kiy").value,
        kd: document.getElementById("kdy").value,
    }
    console.log(campos);
    $.ajax({
        url: '/setCy',
        data: campos,
        type: 'POST',
        success: function(response) {
            console.log(response);
            getPids();
        },
        error: function(error) {
            console.log(error);
        }
    });
})
        $(document).ready(function () {
            var game = true; //Esta variable nos servira para parar el juego una vez terminado
            var cerveza;
            var ws = new WebSocket("ws://localhost:8888/ws"); //cambiar aqui localhost por tu ip
            ws.onopen = function (evt) {
                var conn_status = document.getElementById('conn_text');
                conn_status.innerHTML = "Connection status: Connected!"
            };
            ws.onmessage = function (evt) {
                if (game == true){
                    //aqui recibimos las variables que nos envia el servidor(python tornado)
                    var obj = JSON.parse(evt.data);
                    var mapa = obj.map; //esto es para situar cada objeto en la mapa
                    var message = obj.msg; //aqui esta las posiciones de los coches
                    var status = obj.stat; //esto es el estado de cada jugador, por ejemplo: borracho, pulpo, roca
                    var index = obj.index; //esto nos servira para distinguir un jugador del otro
                    console.log(obj.stat[0]); //no sirve para nada, solo para comprabar que funciona el status
                }
                var coche1 = document.getElementById("coche1");
                var coche2 = document.getElementById("coche2");

                //las posiciones de los coches
                var posfil1 = 20 * parseInt(message[0][0]);
                var poscol1 = 20 * parseInt(message[0][1]);
                coche1.style.left = poscol1 + "px";
                coche1.style.top = posfil1 + "px";
                if (message.length === 2) {
                    var posfil2 = 20 * parseInt(message[1][0]);
                    var poscol2 = 400 + 20 * parseInt(message[1][1]);
                    coche2.style.left = poscol2 + "px";
                    coche2.style.top = posfil2 + "px";
                }

                //el mapa, situa cada objeto en su lugar correspondiente
                var division = document.getElementById("prueba");
                while (division.firstChild) {
                    division.removeChild(division.firstChild); //se va eliminando el mapa anterir y sustituyendo por el nuevo.
                }
                var k, i, j, x;
                for (k = 0; k < mapa.length; k++) {
                    for (i = 0; i < 20; i++) {
                        for (j = 0; j < 10; j++) {
                            if (mapa[k][i][j] === 0) {
                                continue
                            }
                            else if (mapa[k][i][j] === 1) {
                                x = document.createElement("img");
                                x.setAttribute("src", "static/rock.svg");
                            }
                            else if (mapa[k][i][j] === 2) {
                                x = document.createElement("img");
                                x.setAttribute("src", "static/beer.svg");
                            }
                            else if (mapa[k][i][j] === 3) {
                                x = document.createElement("img");
                                x.setAttribute("src", "static/coin.svg");
                            }
                            else if (mapa[k][i][j] === 4) {
                                x = document.createElement("img");
                                x.setAttribute("src", "static/octopus.svg");
                            }
                            else if (mapa[k][i][j] === 5) {
                                x = document.createElement("img");
                                x.setAttribute("src", "static/tirachinas.svg");
                            }
                            x.setAttribute("class", "coches");
                            x.style.top = i * 20 + "px";
                            x.style.left = k * 400 + j * 20 + "px";
                            division.appendChild(x);
                        }
                    }
                }

                //Status oro, aniade un punto si coge un oro, y gana el primero que llege al 10, si los dos llegan la mismo
                //tiempo al 10, es un empate.
                var puntos = [];
                puntos[0] = status[0][2];
                puntos[1] = status[1][2];
                document.getElementById("puntuacion").innerHTML = puntos[0] + ":" + puntos[1];
                if (puntos[0] == 10 && puntos[1] < 10) {
                    document.getElementById("win").textContent = "Player 1 Wins";
                    game = false;
                }
                else if (puntos[1] == 10 && puntos[0] < 10) {
                    document.getElementById("win").textContent = "Player 2 Wins";
                    game = false;
                }
                else if (puntos[1] == 10 && puntos[0] == 10) {
                    document.getElementById("win").textContent = "Tie, Game Over";
                    game = false;
                }
                //tambien gamas si el otro sale del mapa,
                else if (message[0][0] == 20) {
                    document.getElementById("win").textContent = "Player 2 Wins";
                    game = false;
                }
                else if (message[1][0] == 20) {
                    document.getElementById("win").textContent = "Player 1 Wins";
                    game = false;
                }


                //status ropa, al chocar contra una roca, ademas de ser arrastrado hacia abajo(en python), se parpadea.
                if(status[0][0] != 0) {
                    document.getElementById("coche1").classList.add('blink');
                }
                if(status[0][0] == 0) {
                    document.getElementById("coche1").classList.remove('blink');
                }
                if(status[1][0] != 0) {
                    document.getElementById("coche2").classList.add('blink');
                }
                if(status[1][0] == 0) {
                    document.getElementById("coche2").classList.remove('blink');
                }
                //status cerveza(borracho), aqui hemos usado el index porque el efecto de inversion de mando solo se aplica
                //al quien la coge.
                if (status[0][1]==0 && index == 0){
                    cerveza = false
                }
                if (status[0][1]!=0 && index == 0){
                    cerveza = true
                }
                if (status[1][1]==0 && index == 1){
                    cerveza = false
                }
                if (status[1][1]!=0 && index == 1){
                    cerveza = true
                }
                //status pulpo, simplimente activa un div con id pulpoi cuando la coge

                if (status[0][3]==0){
                    document.getElementById("pulpo1").style.opacity = 0;
                }
                if (status[0][3]!=0){
                    document.getElementById("pulpo1").style.opacity = 1;
                }
                if (status[1][3]==0){
                    document.getElementById("pulpo2").style.opacity = 0;
                }
                if (status[1][3]!=0){
                    document.getElementById("pulpo2").style.opacity = 1;
                }

            };

            ws.onclose = function (evt) {
                alert("Connection closed");
            };


            document.onkeydown = checkPress;
            function checkPress(evt) {
                evt = evt || event;
                //Esto envia un mesaje al servidor cuando pulsamos un boton, se distingue cuando esta borracho y cuando no.
                if ((evt.keyCode == 37 && cerveza==false) ||  (evt.keyCode == 39 && cerveza==true)) {
                    evt.preventDefault();
                    var message = 'L';
                    var str1 = `{"msg": "${message || 'default'}" }`;
                    ws.send(str1);
                }
                if ((evt.keyCode == 39 && cerveza==false) || (evt.keyCode == 37 && cerveza==true)) {
                    var message = 'R';
                    evt.preventDefault();
                    var str1 = `{"msg": "${message || 'default'}" }`;
                    ws.send(str1);
                }
                if (evt.keyCode == 32) {
                    var text1 = document.getElementById("text1");
                    text1.style.opacity = 0;
                    var message = 'play';
                    var str1 = `{"go": "${message || 'default'}" }`;
                    ws.send(str1);
                }
            }
        });

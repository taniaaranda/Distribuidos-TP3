function setCookie(usuario,estado){
  var expiracion = new Date();
  expiracion.setDate(expiracion.getDate()+1); //la cookie dura un dia
  document.cookie = nombre + "=" + escape(estado) + "; expires=" +expiracion.toGMTString()+"; path=/";
}

function getCookie(cookie_name) {
  /*
     document.cookie tiene todas las cookies que posee el browser en
     forma de string nombreCookie1=valor1; nombreCookie2=valor2
     */
  var name = cookie_name + "=";
  //handle cookies with special characters
  var decodedCookie = decodeURIComponent(document.cookie);
  var cookie_array = decodedCookie.split(';');
  for(var i = 0; i <cookie_array.length; i++) {
    var c = cookie_array[i];
    while (c.charAt(0) == ' ') {
      c = c.substring(1);
    }
    if (c.indexOf(name) == 0) {
      return c.substring(name.length, c.length); //retorno valor de cookie
    }
  }
  return ""; //cookie not found
}

function loginUser(){ 
  //check cookie
  var username = document.getElementById('username');
  var cookie = getCookie(username.value);
  if (cookie!=""){
    //alert("Bienvenido "+username);
    alert(document.cookie);
  }else{ 
    alert("No tienes cookie");
  }

}


function logoutUser(){
  var users = document.getElementById('users_div');
  var username = document.getElementById('username');
  setCookie(username.value,'inactivo');

  users.innerHTML = unescape(reqObj.responseText); //lo hace submitHandler??
  users.scrollTop = users.scrollHeight;

  alert('Adios '+username.value);
}

//function registrarUser('usrText','targetDiv','users_div','username'){
function registrarUser(){
  var texto = document.getElementById('usrText');
  var target = document.getElementById('targetDiv');
  var users = document.getElementById('users_div');
  var username = document.getElementById('username');
  var reqObj = getReqObj();

  setCookie(username.value,'activo');
  var url="cgi-bin/punto5/registrar_user.py?newtxt="+escape(username.value);
  reqObj.open("GET", url, false);
  reqObj.send(null);
  if (reqObj.responseText == "<p>error</p>"){
    alert("Ha ocurrido un error!. Intenta vuevamente");
  }else if (reqObj.responseText == "<p>ya existe</p>"){
    alert("Ya existe el usuario");
  }else{
    alert(document.cookie);
    users.innerHTML = unescape(reqObj.responseText); //lo hace submitHandler??
    users.scrollTop = users.scrollHeight;
    submitHandler(texo, target); //PRUEBA -- SINO CON usrText,targetDiv
    //texto.disabled=false; //habilito escritura en chat
    var entorno = setInterval(function(){actualizar()},1000);
  }
}

function actualizarConversacion(){
  var conversacion = document.getElementById('divID');
  var reqObj = getReqObj();
  var url="/cgi-bin/punto_5/actualizar_conversacion";
  reqObj.open("GET", url, false);
  reqObj.send(null);
  conversacion.innerHTML = unescape(reqObj.responseText);
  conversacion.scrollTop = conversacion.scrollHeight;
}

function actualizarUsers(){
  var users = getElementById('users_div');
  var reqObj = getReqObj();
  var url="cgi-bin/punto5/actualizar_users.py";
  reqObj.open("GET", url, false);
  reqObj.send(null);
  users.innerHTML = unescape(reqObj.responseText);//innecesario?
  users.scrollTop = users.scrollHeight;
}

function actualizar(){
  actualizarUsers();
  actualizarConversacion();
}

function getReqObj() {
  var XMLHttpRequestObject;
  if (window.XMLHttpRequest) {
    XMLHttpRequestObject = new XMLHttpRequest();
  } else if (window.ActiveXObject) {
    XMLHttpRequestObject = new ActiveXObject("Microsoft.XMLHTTP");
  }
  return XMLHttpRequestObject;
}

function submitHandler(txtID, divID)
{
  var theText = document.getElementById(txtID);
  var theArea = document.getElementById(divID);
  var reqObj = getReqObj();
  var url="/cgi-bin/punto5/textchat?newtxt=" + escape("<p>" + theText.value + "</p>");
  reqObj.open("GET", url, false);
  reqObj.send(null);
  theArea.innerHTML = unescape(reqObj.responseText);
  theArea.scrollTop = theArea.scrollHeight;
  theText.value = "";
  return false;
}

window.onload=function()
{
  document.forms[0][0].focus();
}


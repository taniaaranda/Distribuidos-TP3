#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
Implementacion CGI de login de alumno
Verifica en base de datos "alumnos" los datos que son enviados por el form
Si el usuario existe muestra sus datos para modificacion, sino el login
'''


import sys
import cgi
import cgitb
from collections import deque
import psycopg2

head_html = '''
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8">
    <title>Sistemas Distribuidos</title>
    <link rel="stylesheet" href="css/main.css" type="text/css">
  </head>
  <body>
    <div id="header" align="center">
      <h1> Sistema de gestion de alumnos</h1>
    </div>
    <div class="container">
      <div id="sidebar">
        <ul>
          <li><a href="index.html">Home</a></li>
          <li><a href="alta.html">Alta</a></li>
          <li><a href="modificacion.html">Modificacion</a></li>
        </ul>
      </div>
      <div id="content" >
'''


footer_html = '''
      </div>
    <div align="center">
      <footer class="footer" id="footer">
        <p> Sistemas Distribuidos  - Aranda Perdomo</p>
      </footer>
    </div>
  </body>
</html>

'''


login_html = '''
        <h2> Iniciar sesion </h2>
        <br> <br>
      <form action=/cgi-bin/punto2/login.py method="post">
         Numero de Alumno/Legajo:<br>
          <input type="text" name="legajo" placeholder="9999999"/
                                           max="9999999" required><br><br>
          Password:<br>
          <input type="password" name="password" placeholder="Ingresa clave"
                                                 required><br><br>
          <input type="submit" value="Aceptar">
          <input type="reset" value="Limpiar">
      </form>
'''

modificar_html = '''
      <h2> Crear sesion </h2>
      <form action=/cgi-bin/punto2/modificacion.py method="post">
          Nombre y Apellido:<br>
          <input type="text" name="nombre" placeholder="Nombre y Apellido"/
                                 value="%s" maxlength="70" autofocus required>
          <br><br>
          Numero de Alumno/Legajo:<br>
          <input type="text" name="legajo" placeholder="9999999"/
                            value="%s" max="9999999" required disabled><br><br>
          Sexo:<br>
          <select name="sexo" size="2">
            "%s"
          </select><br><br>
          Edad:<br>
          <input type="number" name="edad" min="1" max="99" value="%s"
          required><br><br>
          Password:<br>
          <input type="password" name="password" placeholder="Ingresa clave"
                                        value="%s" required><br><br>
          <input type="submit" value="Aceptar">
          <input type="reset" value="Limpiar">
      </form>
'''


def obtener_datos(form):
    '''
    obtiene los datos del login.html y se los envia a verificar_alumno
    '''
    legajo = form.getvalue("legajo")
    password = form.getvalue('password')
    values = deque([legajo, password])
    return verificar_alumno(values)


def crear_handler():
    '''
    Crea el objeto conexion y lo retorna
    '''
    connect_str = "dbname='alumnos' user='jtatest' host='localhost'" + \
        " password='jtatest'"
    # use our connection values to establish a connection
    conn = psycopg2.connect(connect_str)
    conn.autocommit = True
    return conn


def destroy_handler(conn):
    '''
    Cierra la conexion, supone que autocommit = True
    '''
    conn.close()


def verificar_alumno(values):
    '''
    Obtiene conexion e verifica que la cola values recibida como parametro,
    exista en tabla alumno .Cierra la conexion al finalizar
    '''
    try:
        conn = crear_handler()
    except psycopg2.Error:
        print ('Error: el servidor no se pudo conectar a la base de datos')
    try:
        cursor = conn.cursor()
        cursor.execute(
            'SELECT * from alumno WHERE legajo=%s AND password=%s',
            (values.popleft(), values.popleft())
        )
        registro = cursor.fetchone()  # obtengo como tupla la fila de la query
        destroy_handler(conn)
        return registro
    except Exception as e:
        print (e)


def parse_sexo_option(sex):
    if sex == "hombre":
        return '''
            <option value="hombre" selected>Hombre</option>
            <option value="mujer">Mujer</option>
            '''
    else:
        return '''
            <option value="hombre">Hombre</option>
            <option value="mujer" selected>Mujer</option>
            '''


def show_html(registro):
    '''
    Elige el formulario que le mostrara al usuario, dependiendo de que values
    (variable que recibe por parametros) contenga datos o no
    '''
    if isinstance(registro, tuple):
        nombre = registro[0]
        legajo = registro[1]
        sexo = parse_sexo_option(registro[2])
        edad = registro[3]
        password = registro[4]
        print(modificar_html % (nombre, legajo, sexo, edad, password))
    else:
        print(login_html)


def main():
    '''
    Intenta dar de alta el alumno y luego muestra
    el html
    '''
    print('Content-Type: text/html')
    print()
    form = cgi.FieldStorage()
    sys.stderr = sys.stdout
    cgitb.enable()
    print(head_html)
    show_html(obtener_datos(form))  # muestra contenido segun corresponda
    print(footer_html)


if __name__ == '__main__':
    main()

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
from http.cookies import SimpleCookie
from datetime import datetime, timedelta
from hashlib import md5
import json
import http
import random


login_html = '''
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8">
    <title>Redirigiendo..</title>
    <meta http-equiv="refresh" content="0;url=/punto2/login.html" />'
  <script>
      alert("Ingrese");
  </script>
  </head>
  <body></body>
</html>
'''

modificar_html = '''
    <!DOCTYPE html>
    <html lang="en">
      <h2> Crear sesion </h2>

      <form action=/cgi-bin/punto2/modificacion.py method="post">
          Nombre y Apellido:<br>
          <input type="text" id="nombre" placeholder="Nombre y Apellido"/
                                 value="%s" maxlength="70" autofocus required>
          <br><br>
          Numero de Alumno/Legajo:<br>
          <input type="text" name="legajo" placeholder="9999999"/
                            value="%s" max="9999999" required readonly><br><br>
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
    <body></body>
    </html>
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


def buscar_alumno(value):
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
            'SELECT * from alumno WHERE legajo='+value
        )
        registro = cursor.fetchone()  # obtengo como tupla la fila de la query
        destroy_handler(conn)
        return registro
    except Exception as e:
        print("error")
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
    nombre = registro[0]
    legajo = registro[1]
    sexo = parse_sexo_option(registro[2])
    edad = registro[3]
    password = registro[4]
    #print(nombre)
    print(modificar_html % (nombre, legajo, sexo, edad, password))


def main():

    print('Content-Type: text/html')
    print()
    data = cgi.FieldStorage()
    query = data.getvalue('newtxt')
    cookie = str(query) + "\n" 
    encontro = False 
    with open("sesioncookies.txt",'r') as f:
        for line in f.readlines():
            id = line[line.find("|")+1:]
            if(id.find(cookie)!= -1):
                legajo= line[:line.find("|")]
                registro=buscar_alumno(legajo) 
                show_html(registro)
                encontro = True
                break
    f.close()
    if(encontro != True):
        print(login_html)


if __name__ == '__main__':
    main()
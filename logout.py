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


htmlFormat = '''
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8">
    <title>Redirigiendo..</title>
    <meta http-equiv="refresh" content="0;url=/punto2/index.html" />'
  <script>
      alert("sesion cerrada");
  </script>
  </head>
  <body></body>
</html>
'''

htmlFormat2 = '''
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8">
    <title>Redirigiendo..</title>
    <meta http-equiv="refresh" content="0;url=/punto2/index.html" />'
  <script>
      alert("no ha iniciado sesion");
  </script>
  </head>
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
    cookie = str(query)
    if(len(cookie)>4): 
        cookie = cookie + "\n"
        encontro = False
        try:
            with open("sesioncookies.txt",'r+') as f:
                lines =f.readlines()
                f.seek(0)
                for line in lines:
                    print(line)
                    id = line[line.find("|")+1:]
                    if(id.find(cookie)!= -1):
                        f.write("")
                        encontro = True
                        break
                f.truncate()
                if(encontro):
                    print(htmlFormat)
                else:
                    print(htmlFormat2)            
            f.close()
        except IOError:
            print("error")
    else:
        print(htmlFormat2)



if __name__ == '__main__':
    main()
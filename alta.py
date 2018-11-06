#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
Implementacion CGI de alta de alumno
Guarda en base de datos "alumnos" los datos que son enviados por el form
'''

import sys
import cgi
import cgitb
from collections import deque
import psycopg2


htmlFormat = '''

<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8">
    <title>Redirigiendo..</title>
    <meta http-equiv="refresh" content="0;url=/punto2" />'
  <script>
      alert("El alumno ha sido creado!");
  </script>
  </head>
  <body></body>
</html>
'''


def dar_alta_alumno(form):
    '''
    Obtiene los datos del form a ingresar en la BD,
    luego se los pasa a insertar_alumno
    '''
    nombre = form.getvalue('nombre')
    legajo = form.getvalue("legajo")
    sexo = form.getvalue('sexo')
    edad = form.getvalue('edad')
    password = form.getvalue('password')
    values = deque([nombre, legajo, sexo, edad, password])
    insertar_alumno(values)


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


def insertar_alumno(values):
    '''
    obtiene conexion e inserta la cola values que recibio en tabla alumno
    cierra la conexion al finalizar
    '''
    try:
        conn = crear_handler()
    except psycopg2.Error:
        print ('Error: el servidor no se pudo conectar a la base de datos')
    try:
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO alumno (nya,legajo,sexo,edad,password)'
            ' VALUES (%s, %s, %s, %s, %s)',
            (values.popleft(), values.popleft(), values.popleft(),
             values.popleft(), values.popleft())
        )
        destroy_handler(conn)
    except Exception as e:
        print (e)


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
    dar_alta_alumno(form)
    print(htmlFormat)


if __name__ == '__main__':
    main()

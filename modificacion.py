#!/usr/bin/python3
# -*- coding: utf-8 -*-


'''
Implementacion CGI de modificacion de alumno
Modifica la base de datos "alumnos" los datos que son enviados por el form
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
    <meta charset="utf-8">
    <title>Redirigiendo..</title>
    <meta http-equiv="refresh" content="0;url=/punto2" />
  <script>
      alert("El alumno ha sido modificado!");
  </script>
  </head>
  <body></body>
</html>
'''


update_sql = """
UPDATE alumno SET (nya,sexo,edad,password)=('%s', '%s', %s, %s) WHERE legajo=%s
"""


def modificar_alumno(form):
    '''
    Obtiene los datos del form para actualizar el alumno en la BD,
    luego se los pasa a update_alumno
    '''
    nombre = form.getvalue('nombre')
    sexo = form.getvalue('sexo')
    edad = form.getvalue('edad')
    password = form.getvalue('password')
    legajo = form.getvalue('legajo')
    values = deque([nombre, sexo, edad, password, legajo])
    update_alumno(values)


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


def update_alumno(values):
    '''
    obtiene conexion y modifica con la cola values que recibio la tabla alumno
    cierra la conexion al finalizar
    '''
    try:
        conn = crear_handler()
    except psycopg2.Error:
        print ('Error: el servidor no se pudo conectar a la base de datos')
    try:
        cursor = conn.cursor()
        cursor.execute(update_sql %
                       (values.popleft(), values.popleft(), values.popleft(),
                        values.popleft(), values.popleft()
                        )
                       )
        destroy_handler(conn)
    except Exception as e:
        print(e)


def main():
    '''
    Modifica los datos del alumno y luego muestra el html
    '''
    print('Content-Type: text/html')
    print()
    form = cgi.FieldStorage()
    sys.stderr = sys.stdout
    cgitb.enable()
    modificar_alumno(form)
    print(htmlFormat)


if __name__ == '__main__':
    main()

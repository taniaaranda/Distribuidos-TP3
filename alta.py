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
    <title>Sistemas Distribuidos</title>
    <link rel="stylesheet" href="http://localhost/punto2/css/main.css"
        type="text/css">
  </head>
  <body>
    <div id="header" align="center">
      <h1> Sistema de gestion de alumnos</h1>
    </div>
    <div class="container">
      <div id="sidebar">
        <ul>
          <li><a href="http://localhost/punto2/index.html">Home</a></li>
          <li><a href="http://localhost/punto2/alta.html">Alta</a></li>
          <li><a href="http://localhost/punto2/login.html">
                            Modificacion</a></li>
          <li><a href="http://localhost/punto2/busquedas.html">Busquedas</a>
          </li>
          <li><a href="http://localhost/punto2/listas.html">Totales</a></li>
        </ul>
      </div>
      <div id="content" >
        <form action=/cgi-bin/punto2/alta.py method="post">
          Nombre y Apellido:<br>
          <input type="text" name="nombre" placeholder="Nombre y Apellido"/
                                 maxlength="70" autofocus required><br><br>
          Numero de Alumno/Legajo:<br>
          <input type="text" name="legajo" placeholder="9999999"/
                                           max="9999999" required><br><br>
          Sexo:<br>
          <select name="sexo" size="2">
            <option value="hombre">Hombre</option>
            <option value="mujer">Mujer</option>
          </select><br><br>
          Edad:<br>
          <input type="number" name="edad" min="1" max="99" required><br><br>
          Password:<br>
          <input type="password" name="password" required><br><br>
          <input type="submit" value="Aceptar">
          <input type="reset" value="Limpiar">
        </form>
      </div>
    </div>
    <div align="center">
      <footer class="footer" id="footer">
        <p> Sistemas Distribuidos  - Aranda Perdomo</p>
      </footer>
    </div>
  </body>
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

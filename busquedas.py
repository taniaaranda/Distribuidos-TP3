#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
Implementacion CGI de busqueda de alumnos
Busca en base de datos "alumnos" los datos que son enviados por el form
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
        <table>
          <tr>
            <th>Nombre</th>
            <th>Legajo</th>
            <th>Sexo</th>
            <th>Edad</th>
          </tr>
'''


footer_html = '''
      </table>
    </div>
    <div align="center">
      <footer class="footer" id="footer">
        <p> Sistemas Distribuidos  - Aranda Perdomo</p>
      </footer>
    </div>
  </body>
</html>

'''

encontre_html = '''
<tr>
<td>%s</td>
<td>%s</td>
<td>%s</td>
<td>%s</td>
</tr>
'''

no_encontre_html = '''
'''

select_sql = '''
SELECT * FROM alumno WHERE %s
'''


def obtener_datos(form):
    '''
    obtiene el campo a buscar del arhcivo html y se los envia a realizar_query
    '''
    campo = form.getvalue('campo')
    valor = form.getvalue('buscar')
    values = deque([campo, valor])
    return realizar_query(values)


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


def parsear_intervalo(valor):
    '''
    Parsea el valor que recibe por parametro y luego retorna la condicion de
    una consulta sql en la que hay un intervalo numerico
    Puede ser que exista un intervalo o no, es decir (min - max) o (valor)
    '''
    if '-' in valor:
        minimo, maximo = valor.split("-", 1)
        return ' BETWEEN {0} AND {1}'.format(minimo, maximo)
    else:
        return '={0}'.format(valor)


def parsear_random(valor):
    '''
    Parsea el valor que recibe por parametro y retorna la condicion de una
    consulta sql en la que puede o no existir una busqueda con pattern = *, es
    decir que es posible realizar una busqueda en sql con atributo "%"
    '''
    if '*' in valor:
        return valor.replace('*', '%')
    else:
        return valor


def get_cond_skeleton(campo, valor):
    '''
    Segun el campo que reciba retorna el esqueleto de una condicion
    de una query sql utilizando el valor a buscar.
    Es decir que retorna lo que iria dentro de una condicion WHERE en SQL
    '''
    if campo == 'edad':
        return 'edad' + parsear_intervalo(valor)
    elif campo == 'nombre':
        return "nya LIKE '" + (parsear_random(valor)) + "'"
    elif campo == 'sexo':
        return "sexo='" + valor + "'"
    else:
        return 'legajo ' + parsear_intervalo(valor)


def realizar_query(values):
    '''
    Obtiene conexion e verifica que la cola values recibida como parametro,
    exista en tabla alumno .Cierra la conexion al finalizar
    '''
    try:
        conn = crear_handler()
    except psycopg2.Error:
        print ('Error: el servidor no se pudo conectar a la base de datos')
    try:
        campo = values.popleft()
        valor = values.popleft()
        # print(select_sql % get_cond_skeleton(campo, valor))
        cursor = conn.cursor()
        cursor.execute(select_sql % get_cond_skeleton(campo, valor))
        # select * from alumno where nombre like "%Borges%";
        # select * from alumno WHERE number BETWEEN @start AND @end
        registros = cursor.fetchall()  # obtengo todas las filas de la query
        mostrar_valores(registros)
        destroy_handler(conn)
    except Exception as e:
        print (e)


def mostrar_valores(registros):
    '''
    Recorre los registos y mientras tenga datos los muestra a traves de
    show_html
    '''
    if isinstance(registros, list):
        for record in registros:
            show_html(record)
    else:
        print(no_encontre_html)


def show_html(registro):
    '''
    Elige el formulario que le mostrara al usuario, dependiendo de que values
    (variable que recibe por parametros) contenga datos o no
    '''
    if isinstance(registro, tuple):
        nombre = registro[0]
        legajo = registro[1]
        sexo = registro[2]
        edad = registro[3]
        print(encontre_html % (nombre, legajo, sexo, edad))


def main():
    '''
    Busca el alumno y luego muestra el html
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

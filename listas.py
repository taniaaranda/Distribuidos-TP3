#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
Implementacion CGI de listados por totales de alumnos
Consulta en base de datos "alumnos" los datos que son enviados por el form
'''

import sys
import cgi
import cgitb
from collections import deque
import psycopg2


head_html = '''
    <a href="/punto2">Click para voler al index</a>
    <hr width="80%" size=3 align="left" noshade>
'''


mostrar_html = '''
    <table border="1"cellpadding = "5" cellspacing = "5">
      <tr>
        <th>Sexo</th>
        <th>Total</th>
        <th>Promedio</th>
      </tr>
      <tr>
        <td>%s</td>
        <td>%s</td>
        <td>%s</td>
      </tr>
    </table>
    <br>
'''

select_sql = '''
SELECT sexo, count(*), avg(edad) FROM alumno WHERE %s GROUP BY sexo
'''


def obtener_datos(form):
    '''
    obtiene el intervalo de edades a buscar y el sexo de los alumnos del
    arhcivo html y se los envia a realizar_query
    '''
    intervalo = form.getvalue('intervalo')
    sexo = form.getvalue('sexo')
    values = deque([intervalo, sexo])
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
    '''
    if valor == 'primer_grupo':
        return ' < 20'
    elif valor == 'segundo_grupo':
        return ' BETWEEN 20 AND 40'
    else:
        return ' > 40'


def get_cond_skeleton(intervalo, sexo):
    '''
    Segun el intervalo de edades y el sexo que reciba retorna el esqueleto de
    una condicion de una query sql utilizando el valor a buscar.
    Es decir que retorna lo que iria dentro de una condicion WHERE en SQL
    '''
    return "sexo='" + sexo + "' AND edad " + parsear_intervalo(intervalo)


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
        cursor = conn.cursor()
        cursor.execute(select_sql % get_cond_skeleton(campo, valor))
        registro = cursor.fetchone()  # obtengo la tupla de la query
        show_html(registro)
        destroy_handler(conn)
    except Exception as e:
        print (e)


def show_html(registro):
    '''
    Elige el formulario que le mostrara al usuario, dependiendo de que values
    (variable que recibe por parametros) contenga datos o no
    '''
    if isinstance(registro, tuple):
        sexo = registro[0]
        cont = registro[1]
        avg = registro[2]
        print(mostrar_html % (sexo, cont, avg))


def main():
    '''
    Busca totales de alumnos y luego muestra el html
    '''
    print('Content-Type: text/html')
    print()
    form = cgi.FieldStorage()
    sys.stderr = sys.stdout
    cgitb.enable()
    print(head_html)
    show_html(obtener_datos(form))  # muestra contenido segun corresponda


if __name__ == '__main__':
    main()

#!/usr/bin/python3
# -*- coding: utf-8 -*-

import cgi


def existe_usuario(usuario):
    try:
        with open("/tmp/usuarios.txt", "r") as f:
            for line in f:
                if(line.find(usuario) != -1):
                    f.close()
                    return True
        f.close()
        return False
    except IOError:  # no existe el archivo
        return False


def main():
    print('Content-Type: text/html')
    print()
    data = cgi.FieldStorage()
    query = data.getvalue('newtxt')
    user = str(query)
    if(existe_usuario(user)):
        print("<p>error</p>")
    else:
        with open("/tmp/usuarios.txt", 'a+') as f:
            # mode a+ crea el archivo si no existe
            f.write(user)
        f.close()


if __name__ == '__main__':
    main()
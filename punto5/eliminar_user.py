#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import cgi


def existe_usuario(usuario):
    try:
        usuario = usuario + '\n'
        with open("data/usuarios.txt", 'r+') as f:
            lines = f.readlines()
            f.seek(0)
            for i in lines:
                if(i.find(usuario) == -1):
                    f.write(i)
            f.truncate()
            f.close()
            return True
        f.close()
        return False
    except IOError:  # no existe el archivo
        print("no existe")
        return False


def check_usuarios():
    '''
    En caso de que no queden usuarios en el chat, elimina la conversacion
    '''
    print('lines blank..')
    print('verificando size..')
    if os.path.getsize('data/usuarios.txt') == 0:
        # open('data/chat.txt', 'w').close()
        print ('antes : %s' % os.path.getsize('data/chat.txt'))
        os.remove('data/chat.txt')
        print ('size: %s' % os.path.getsize('data/chat.txt'))


def main():
    print('Content-Type: text/html')
    print()
    data = cgi.FieldStorage()
    query = data.getvalue('newtxt')
    user = str(query)
    if(existe_usuario(user)):
        print("<p>sesion cerrada</p>")
    else:
        print("<p>error</p>")
    check_usuarios()


if __name__ == '__main__':
    main()

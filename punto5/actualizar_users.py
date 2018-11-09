#!/usr/bin/python3
# -*- coding: utf-8 -*-


def main():
    print('Content-Type: text/html')
    print()
    try:
        with open("data/usuarios.txt", 'r') as f:
            for line in f.readlines():
                print(line)
        f.close()
    except IOError:
        print("No existe usuarios")


if __name__ == '__main__':
    main()

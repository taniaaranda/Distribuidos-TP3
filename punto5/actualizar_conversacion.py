#!/usr/bin/python3
# -*- coding: utf-8 -*-


def main():
    print('Content-Type: text/html')
    print()
    with open('data/chat.txt', 'r') as f:
        for line in f.readlines():
            print(line)
    f.close()


if __name__ == '__main__':
    main()

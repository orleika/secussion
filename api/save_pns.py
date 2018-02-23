# -*- coding: utf-8 -*-
from sys import argv
from db import DB

def main():
    file_name = argv[1]
    f = open(file_name)
    db = DB(host = 'mysql')
    for line in f.read().splitlines():
        d = line.split(':')
        db.save_pn(surface = d[0], reading = d[1], pos = d[2], score = d[3])
    f.close()

if __name__ == '__main__':
    main()

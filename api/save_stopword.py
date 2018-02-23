# -*- coding: utf-8 -*-
from sys import argv
from db import DB

def main():
    file_name = argv[1]
    f = open(file_name)
    db = DB(host = 'mysql')
    for word in f.read().splitlines():
        db.save_stopword(word = word)
    f.close()

if __name__ == '__main__':
    main()

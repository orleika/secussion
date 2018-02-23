# -*- coding: utf-8 -*-
import mysql.connector
from collections import namedtuple

Wnet = namedtuple('Wnet', 'id, word, layer, pos, parent_id, created_at, updated_at')

class DB:

    def __init__(self, host = 'localhost', port = '3306', user = 'docker', password = 'password', database = 'app'):
        conn = mysql.connector.connect(
            host = host,
            port = port,
            user = user,
            password = password,
            database = database,
        )
        conn.ping(True)
        self.conn = conn

    def connect(self):
        self.conn = mysql.connector.connect()

    def save(self, word = '', layer = '', pos = '', parent_id = 1):
        cursor = self.conn.cursor()
        sql = ("INSERT INTO wnet "
                      "(word, layer, pos, parent_id) "
                      "VALUES (%(word)s, %(layer)s, %(pos)s, %(parent_id)s)")
        data = {
            'word': word,
            'layer': layer,
            'pos': pos,
            'parent_id': parent_id,
        }
        cursor.execute(sql, data)
        self.conn.commit()
        cursor.close()

    def get_dfs(self):
        cursor = self.conn.cursor()
        sql = ("SELECT * FROM dfs")
        cursor.execute(sql)
        df = namedtuple('Df', 'id, word, count')
        results = []
        for row in cursor:
            results.append(df(row[0], row[1], row[2]))
        cursor.close()
        return results

    def save_df(self, word = ''):
        cursor = self.conn.cursor()
        sql = ("INSERT INTO dfs (word, count) "
                "VALUES (%(word)s, 1) "
                "ON DUPLICATE KEY UPDATE count = count + 1")
        data = {
            'word': word,
        }
        cursor.execute(sql, data)
        cursor.close()

    def get_stopwords(self):
        cursor = self.conn.cursor()
        sql = ("SELECT * FROM stopwords")
        cursor.execute(sql)
        stopword = namedtuple('Stopword', 'id, word')
        results = []
        for row in cursor:
            results.append(stopword(row[0], row[1]))
        cursor.close()
        return results

    def save_stopword(self, word = ''):
        cursor = self.conn.cursor()
        sql = ("INSERT INTO stopwords "
                      "(word) "
                      "VALUES (%(word)s)")
        data = {
            'word': word,
        }
        cursor.execute(sql, data)
        self.conn.commit()
        cursor.close()

    def all(self):
        cursor = self.conn.cursor()
        sql = ("SELECT * FROM wnet "
                "WHERE deleted_at IS NULL")
        cursor.execute(sql)
        results = []
        for row in cursor:
            results.append(Wnet(row[0], row[1], row[2], row[3], row[4], row[5], row[6]))
        cursor.close()
        return results

    def word_search(self, word = ''):
        cursor = self.conn.cursor()
        sql = ("SELECT * FROM wnet "
                "WHERE word = %(word)s AND deleted_at IS NULL")
        data = {
            'word': word
        }
        cursor.execute(sql, data)
        results = []
        for row in cursor:
            results.append(Wnet(row[0], row[1], row[2], row[3], row[4], row[5], row[6]))
        cursor.close()
        return results

    def exist_word(self, word = ''):
        return len(self.word_search(word)) != 0

    def max_layer_words(self):
        cursor = self.conn.cursor()
        sql = ("SELECT * FROM wnet "
                "WHERE layer = (SELECT MAX(layer) FROM wnet) AND deleted_at IS NULL")
        cursor.execute(sql)
        results = []
        for row in cursor:
            results.append(Wnet(row[0], row[1], row[2], row[3], row[4], row[5], row[6]))
        cursor.close()
        return results

    def root(self):
        cursor = self.conn.cursor()
        sql = ("SELECT * FROM wnet "
                "WHERE layer = 1 AND deleted_at IS NULL")
        cursor.execute(sql)
        results = []
        for row in cursor:
            results.append(Wnet(row[0], row[1], row[2], row[3], row[4], row[5], row[6]))
        cursor.close()
        return results

    def parent_word(self, word = ''):
        cursor = self.conn.cursor()
        sql = ("SELECT * FROM wnet "
                "WHERE id = (SELECT parent_id FROM wnet WHERE word = %(word)s LIMIT 1) AND deleted_at IS NULL")
        data = {
            'word': word
        }
        cursor.execute(sql, data)
        results = []
        for row in cursor:
            results.append(Wnet(row[0], row[1], row[2], row[3], row[4], row[5], row[6]))
        cursor.close()
        return results[0]

    def __del__(self):
        self.conn.close()

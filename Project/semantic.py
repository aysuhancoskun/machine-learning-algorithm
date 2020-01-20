# -*- coding: utf-8 -*-
import sqlite3
con = sqlite3.connect('semantic.db')
cursor = con.cursor()
def create_table():
  cursor.execute('''CREATE TABLE IF NOT EXISTS nouns(id1 INTEGER PRIMARY KEY, noun TEXT)''')
  con.commit()


def create_table():
  cursor.execute('''CREATE TABLE IF NOT EXISTS verb(id2 INTEGER PRIMARY KEY, verb TEXT)''')
  con.commit()

  
def create_table():
  cursor.execute('''CREATE TABLE IF NOT EXISTS join(noun1_id INTEGER,noun2_id INTEGER,verb_id INTEGER)''')
  con.commit()

def insert_value(id,noun):
    cursor.execute("INSERT INTO nouns VALUES('1111','dog')")
    cursor.execute("INSERT INTO nouns VALUES('2222','cat')")
    con.commit()

def insert_value(id,verb):
    cursor.execute("INSERT INTO verb VALUES('3333','bark')")
    con.commit()

    
def insert_value(noun1_id,noun2_id,verb_id):
    cursor.execute("INSERT INTO join VALUES('1111','2222','3333')")
    con.commit()



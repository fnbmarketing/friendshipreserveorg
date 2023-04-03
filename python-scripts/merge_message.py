#!/usr/bin/env python3


import sqlite3

conn = sqlite3.connect('/Users/danipan/Desktop/Friendship-Reserve/chat.db')

c = conn.cursor()

c.execute('CREATE TABLE merged_egg_2023_q1 AS SELECT date, text, phone_number FROM oldegg UNION SELECT date, text, phone_number FROM Newegg')

conn.commit()
conn.close()

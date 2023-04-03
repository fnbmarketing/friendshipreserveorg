#!/usr/bin/env python3


import sqlite3
import sys

conn = sqlite3.connect('/Users/danipan/Desktop/Friendship-Reserve/chat.db')

c = conn.cursor()


def update_date_column(table_name):
    # Update the date column
    c.execute("UPDATE {} SET date = strftime('%Y-%m-%d %H:%M:%S', datetime(date/1000000000 + strftime('%s', '2001-01-01 00:00:00', 'utc'), 'unixepoch', 'localtime'))".format(table_name))

    # Commit the changes and close the connection
    conn.commit()
    conn.close()


if __name__ == '__main__':
    # Read the command-line arguments
    if len(sys.argv) != 2:
        print("Usage: python fix_date_humanreadable.py [table_name]")
        sys.exit(1)

    table_name = sys.argv[1]

update_date_column(table_name)


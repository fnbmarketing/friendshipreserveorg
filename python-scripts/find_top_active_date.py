#!/usr/bin/env python3

import sqlite3
import sys

def get_top_dates(table_name):
    # Connect to the database
    conn = sqlite3.connect('/Users/danipan/Desktop/Friendship-Reserve/chat.db')
    c = conn.cursor()

    # Execute the SQL query to extract the count of rows for each date in Q1 2023
    c.execute("""
        SELECT DATE(date) as date_only, COUNT(*) as count 
        FROM {} 
        WHERE date >= '2023-01-01' AND date < '2023-04-01'
        GROUP BY date_only 
        ORDER BY count DESC 
        LIMIT 10
    """.format(table_name))

    # Fetch the results
    results = c.fetchall()

    # Close the cursor and connection
    c.close()
    conn.close()

    # Return the results as a list of tuples
    return results

if __name__ == '__main__':
    # Read the command-line arguments
    if len(sys.argv) != 2:
        print("Usage: python get_top_dates.py [table_name]")
        sys.exit(1)

    table_name = sys.argv[1]

    # Call the get_top_dates function to query the top dates in the specified table within Q1 2023
    results = get_top_dates(table_name)

    # Print the results
    for row in results:
        print(row[0], row[1])


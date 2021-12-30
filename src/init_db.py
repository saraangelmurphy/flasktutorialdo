import sqlite3
# Open a connection to a database file called database.db. Will be created when the script runs.
connection = sqlite3.connect('database.db')
# Opens the schema, and executes the content of the schema using the executescript method
# This method allows you to execute multiple SQL statements at once; specifically, we drop the posts table if it exists and create it anew
with open('schema.sql') as f:
    connection.executescript(f.read())
    
# Creates a cursor object, which has methods to execute SQL statements
cur = connection.cursor()

cur.execute("INSERT INTO posts (title, content) VALUES (?, ?)",
            ('First Post', 'Content for first post')
            )

cur.execute("INSERT INTO posts (title, content) VALUES (?, ?)",
            ('Second Post', 'Content for Second post')
            )

# We commit our statements and close the connection to the database
connection.commit()
connection.close()
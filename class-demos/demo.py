import psycopg2

# Establish a connection, starting a session, begins a transaction
connection = psycopg2.connect('dbname=example')

# Open a cursor to perform database operations
cursor = connection.cursor()

cursor.execute('DROP TABLE IF EXISTS table2;')

cursor.execute('''
  CREATE TABLE table2 (
    id INTEGER PRIMARY KEY,
    completed BOOLEAN NOT NULL DEFAULT False
  );
''')

cursor.execute('INSERT INTO table2 (id, completed) VALUES (0, false);')

cursor.execute('INSERT INTO table2 (id, completed) VALUES (%s, %s);', (1, True))

SQL = 'INSERT INTO table2 (id, completed) VALUES (%(id)s, %(completed)s);'

data = {
  'id': 2,
  'completed': False
}
cursor.execute(SQL, data)

cursor.execute('SELECT * from table2;')

# fetches the first result in the result set
result2 = cursor.fetchone()
print('fetchone', result2)

result3 = cursor.fetchmany(1)
print('fetchmany(2)', result3)

result = cursor.fetchall()
print('fetchall', result)

# commit, so it does the executions on the db and persists in the db
connection.commit()

# rollback the transaction
# connection.rollback()

cursor.close()
# close the connection (not done automatically)
connection.close()


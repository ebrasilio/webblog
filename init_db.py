import sqlite3      # gerenciador de banco de dados

connection = sqlite3.connect('database.db')  # conecta ao banco 

with open('schema.sql') as f:                # roda o script para criar as tabelas 
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO posts (title, content) VALUES (?,?)",   # inseri dados 
            ('First Post','Content for the first cost'))

cur.execute("INSERT INTO posts (title, content) VALUES (?,?)",    # inseri dados
            ('Second Post', 'Content for the second post'))

connection.commit()                                              # comita as inserções
connection.close()                                               # fecha a conexão
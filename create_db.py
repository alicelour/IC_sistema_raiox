import sqlite3

# Cria um banco de dados e uma tabela de usuários
conn = sqlite3.connect('users.db')
c = conn.cursor()
c.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
    )
''')
# Insira um usuário de exemplo
c.execute("INSERT OR IGNORE INTO users (username, password) VALUES (?, ?)", ("aaa", "123"))
c.execute("INSERT OR IGNORE INTO users (username, password) VALUES (?, ?)", ("aaaa", "1234"))
c.execute("INSERT OR IGNORE INTO users (username, password) VALUES (?, ?)", ("aaaa", "12345"))
conn.commit()
conn.close()

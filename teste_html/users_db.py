import sqlite3

# Criando a base de dados e a tabela de usuários
conn = sqlite3.connect('users.db')
c = conn.cursor()
c.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        password TEXT NOT NULL
    )
''')



def create_items_table():
    # Conecta ao banco de dados (ou cria se não existir)
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    # Cria a tabela de itens, se ela ainda não existir
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            price REAL
        )
    ''')

def create_items2_table():
    # Conecta ao banco de dados (ou cria se não existir)
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    # Cria a tabela de itens, se ela ainda não existir
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            price REAL
        )
    ''')

conn.commit()
conn.close()

if __name__ == '__main__':
    create_items_table()
    print("Tabela 'items' criada com sucesso!")
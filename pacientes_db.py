import sqlite3

# Criando a base de dados e a tabela de pacientes
"""conn = sqlite3.connect('pacientes.db')
c = conn.cursor()
c.execute('''
    CREATE TABLE IF NOT EXISTS pacientes (
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        patient_name TEXT NOT NULL, 
        idade INTEGER, 
        sexo TEXT NOT NULL,
        diagnostico REAL,
        caminho_imagem TEXT
    )
''')"""

#Crie o banco de dados pacientes_removidos.db]
conn = sqlite3.connect('pacientes.db')
c = conn.cursor()
c.execute('''
    CREATE TABLE IF NOT EXISTS pacientes_removidos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_name TEXT NOT NULL,
        idade INTEGER,
        sexo TEXT,
        diagnostico REAL,
        caminho_imagem TEXT
        filename_cam TEXT NOT NULL
    )
''')
conn.commit()
conn.close()
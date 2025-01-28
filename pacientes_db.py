import sqlite3

# Criando a base de dados e a tabela de pacientes
conn = sqlite3.connect('pacientes.db')
c = conn.cursor()
c.execute('''
    CREATE TABLE IF NOT EXISTS pacientes (
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        patient_name TEXT NOT NULL,  
        diagnostico_texto TEXT NOT NULL
    )
''')


conn.commit()
conn.close()
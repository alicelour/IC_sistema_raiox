import sqlite3

banco = sqlite3.connect('pacientes.db')
cursor = banco.cursor()

#cursor.execute("CREATE TABLE IF NOT EXISTS pacientes (id, nome, diagnostico, idade, sexo)")




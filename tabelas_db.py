import sqlite3

banco = sqlite3.connect('pacientes.db')
cursor = banco.cursor()

'''
CREATE TABLE pacientes (
    id TEXT NOT NULL,
    nome TEXT NOT NULL,
    diagnostico TEXT NOT NULL,
    idade INTEGER,
    sexo TEXT NOT NULL
    CREATE TABLE pacientes (
    id TEXT NOT NULL,
    nome TEXT NOT NULL,
    diagnostico TEXT NOT NULL,
    idade INTEGER,
    sexo TEXT NOT NULL,
    link TEXT
);

'''


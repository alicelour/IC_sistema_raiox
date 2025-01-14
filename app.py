from flask import Flask, render_template, request, redirect, url_for, flash, session
import sqlite3
import secrets
import os
import pydicom
from rede import Modelo  # Aqui você importa a classe que contém a sua rede neural, adaptada para o seu caso.

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

# Função para conectar ao banco de dados
def get_db_connection():
    conn = sqlite3.connect('users.db')
    conn.row_factory = sqlite3.Row
    return conn

# Função para obter pacientes do banco de dados
def obter_pacientes():
    conexao = sqlite3.connect('pacientes.db')
    cursor = conexao.cursor()
    cursor.execute('SELECT id, patient_name, patient_id, diagnostico_texto FROM pacientes')
    pacientes = cursor.fetchall()
    conexao.close()
    return pacientes

# Função para obter um paciente específico
def obter_paciente(id):
    conexao = sqlite3.connect('pacientes.db')
    cursor = conexao.cursor()
    cursor.execute('SELECT * FROM pacientes WHERE id = ?', (id,))
    paciente = cursor.fetchone()
    conexao.close()
    return paciente

# Função para rodar a rede neural e obter o diagnóstico
def rodar_rede(file_path):
    modelo = Modelo(r"C:\Users\alice\Downloads\PERFUSAO_PULM_CORONAL_1302\IM-0011-0007.dcm")
    diagnostico = modelo.predict(file_path)  # Passa o caminho do arquivo aqui
    return diagnostico  # Retorna o diagnóstico

def show_dicom_info(file, diagnostico):

    # Carrega o arquivo DICOM
    ds = pydicom.dcmread(file)
    diagnostico_texto = "COVID" if diagnostico == 1 else "Sem COVID"


    # Obtém os metadados do DICOM
    patient_name = ds.get("PatientName", "N/A")
    patient_id = ds.get("PatientID", "N/A")

    # Salva os dados no banco de dados
    conn = sqlite3.connect("pacientes.db")  # Nome do banco de dados
    cursor = conn.cursor()

    # Cria a tabela caso não exista
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS pacientes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_name TEXT,
        patient_id TEXT,
        diagnostico_texto TEXT
    )
    """)

    # Insere os dados no banco
    cursor.execute("""
    INSERT INTO pacientes (patient_name, patient_id, diagnostico_texto)
    VALUES (?, ?, ?)
    """, (str(patient_name), str(patient_id), diagnostico_texto))

    # Confirma a transação e fecha a conexão
    conn.commit()
    conn.close()

    print("Informações do DICOM e diagnóstico salvos no banco de dados com sucesso!")

# Rota para a página de login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Conectando ao banco de dados e buscando o usuário
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password)).fetchone()
        conn.close()
        
        if user:
            session['user_id'] = user['id']
            flash('Login realizado com sucesso!')
            return redirect(url_for('dashboard'))
        else:
            flash('Nome de usuário ou senha inválidos!')
            return redirect(url_for('login'))

    return render_template('login.html')

# Rota para a página principal após login
@app.route('/dashboard')
def dashboard():
    pacientes = obter_pacientes()
    return render_template('dashboard.html', pacientes=pacientes)

# Rota para visualizar o detalhe do paciente
@app.route('/detalhe/<int:id>')
def detalhe(id):
    paciente = obter_paciente(id)
    
    if request.method == 'POST':
        file = request.files['dicom_file']  # Arquivo DICOM enviado pelo usuário
        file_path = os.path.join('uploads', file.filename)
        file.save(file_path)
        diagnostico = rodar_rede(file_path)
        
        diagnostico_texto = "COVID" if diagnostico == 1 else "Sem COVID"
        
        # Atualiza o diagnóstico no banco de dados
        conn = sqlite3.connect('pacientes.db')
        cursor = conn.cursor()
        cursor.execute('UPDATE pacientes SET diagnostico_texto = ? WHERE id = ?', (diagnostico_texto, id))
        conn.commit()
        conn.close()
        
        flash('Diagnóstico atualizado com sucesso!')
        return redirect(url_for('detalhe', id=id))
    
    return render_template('detalhe.html', paciente=paciente)

if __name__ == '__main__':
    app.run(debug=True)

   
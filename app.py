from flask import Flask, render_template, request, redirect, url_for, flash, session
import sqlite3
import secrets
import os
import pydicom
from predict import ImagePredictor


app = Flask(__name__)
app.secret_key = secrets.token_hex(16)


# Função para conectar ao banco de dados
def get_db_connection():
    conn = sqlite3.connect('users.db')
    conn.row_factory = sqlite3.Row
    return conn


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

@app.route('/processar_imagens', methods=['POST'])
def processar_imagens():
    pasta_imagens = r"C:\Users\alice\teste"
    feature_extractor_path = r"C:\Users\alice\Downloads\feature_extractor (1).h5"
    model_path = r"C:\Users\alice\Downloads\fuzzy_model.h5"
    
    predictor = ImagePredictor(feature_extractor_path, model_path)
    
    conn = get_db_connection_pacientes()
    cursor = conn.cursor()

    for filename in os.listdir(pasta_imagens):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            image_path = os.path.join(pasta_imagens, filename)
            prediction = predictor.predict_image(image_path)  # Obtém a predição da imagem

            nome_paciente = os.path.splitext(filename)[0]  # Nome do arquivo como nome do paciente
            
            # Verifica se o paciente já existe no banco
            cursor.execute("SELECT * FROM pacientes WHERE patient_name = ?", (nome_paciente,))
            paciente_existente = cursor.fetchone()

            if not paciente_existente:
                cursor.execute("INSERT INTO pacientes (patient_name, diagnostico_texto) VALUES (?, ?)", (nome_paciente, str(prediction)))
    
    conn.commit()
    conn.close()
    
    flash('Imagens processadas e pacientes atualizados!')
    return redirect(url_for('dashboard'))

def get_db_connection_pacientes():
    conn = sqlite3.connect('pacientes.db')  # Troquei users.db para pacientes.db
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/dashboard')
def dashboard():
    conn = get_db_connection_pacientes()
    # Modificando a consulta SQL para ordenar os pacientes de forma decrescente pelo diagnóstico
    pacientes = conn.execute("SELECT * FROM pacientes ORDER BY diagnostico_texto DESC").fetchall()
    # Separar pacientes de alta prioridade
    alta_prioridade = []
    outros_pacientes = []
    
    for paciente in pacientes:
        try:
            valor = float(paciente['diagnostico_texto'])
            if valor >= 0.7:
                alta_prioridade.append(paciente)
            else:
                outros_pacientes.append(paciente)
        except ValueError:
            outros_pacientes.append(paciente)
            
    conn.close()

    return render_template('dashboard.html', alta_prioridade=alta_prioridade, outros_pacientes=outros_pacientes)

# Rota para visualizar o detalhe do paciente
@app.route('/detalhe/<int:id>')
def detalhe(id):

    return redirect(url_for('detalhe', id=id))
    

if __name__ == '__main__':
    app.run(debug=True)

   
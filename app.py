from flask import Flask, render_template, request, redirect, url_for, flash, session
import sqlite3
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

# Função para conectar ao banco de dados

def get_db_connection(): #está definindo uma função que não recebe parâmetros.responsável por criar e retornar uma conexão com o banco de dados SQLite.
    conn = sqlite3.connect('users.db')   #abrir um arquivo de banco de dados chamado users.db
    conn.row_factory = sqlite3.Row
    return conn

# Rota para a página de login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':  #Se for uma requisição do tipo POST, significa que o usuário enviou o formulário de login e os dados precisam ser processados.
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
    if 'user_id' in session:
        return render_template('dashboard.html')
    else:
        return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)

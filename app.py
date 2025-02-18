from flask import Flask, render_template, request, redirect, url_for, flash, session
import sqlite3
import secrets
import os
import pydicom
from predict import ImagePredictor
import pydicom
import imageio
from skimage import exposure


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

# Função que processa imagens DICOM e envia para a rede neural
def processar_imagens():


    pasta_dicom = r"C:\Users\alice\teste_html\dicom"  # Pasta onde estão os arquivos DICOM
    pasta_uploads = r"C:\Users\alice\teste_html\static\uploads"    # Pasta para salvar os PNGs
    os.makedirs(pasta_uploads, exist_ok=True)    # Cria a pasta se não existir

    feature_extractor_path = r"C:\Users\alice\Downloads\feature_extractor (1).h5"
    model_path = r"C:\Users\alice\Downloads\fuzzy_model.h5"

    predictor = ImagePredictor(feature_extractor_path, model_path)


    count=0

    for filename in os.listdir(pasta_dicom):
        count+=1
        print("\n")

        if filename.lower().endswith('.dcm'):
            dicom_path = os.path.join(pasta_dicom, filename)
            print("")

            # Carregar imagem DICOM
            ds = pydicom.dcmread(dicom_path)

            # Extrair informações do paciente dos metadados DICOM
            nome_paciente = nome_paciente = str(ds.get("PatientName"))
            idade = ds.get("PatientAge")  
            sexo = ds.get("PatientSex")  

            # Ajustar idade para remover 'Y' no final, se existir
            if isinstance(idade, str) and idade.endswith("Y"):
                idade = idade[:-1]  # Remove o 'Y' da idade

            # Processar a imagem
            pixel_array = ds.pixel_array
            pixel_array = exposure.rescale_intensity(pixel_array, out_range=(0, 255))

            # Salvar a imagem como PNG na pasta "uploads"
            png_filename = f"{count}.png"
            png_path = os.path.join(pasta_uploads, png_filename)
            caminhobd= f"uploads/{count}.png"
            print(f"Salvando imagem em: {png_path}")  # Debug

            # Salvar o arquivo PNG
            imageio.imwrite(png_path, pixel_array.astype("uint8"))

            # Fazer a predição usando a rede neural
            prediction = predictor.predict_image(png_path)
            print(prediction)
            prediction = float(prediction)  # Converte para float

            conn = get_db_connection_pacientes()
            cursor = conn.cursor()

            # Verificar se o paciente já está cadastrado no banco
            cursor.execute("SELECT * FROM pacientes WHERE caminho_imagem = ?", (caminhobd,))
            paciente_existente = cursor.fetchone()

            if not paciente_existente:
                try:
                    cursor.execute("""
                        INSERT INTO pacientes (patient_name, idade, sexo, diagnostico, caminho_imagem, filename_dcm)
                        VALUES (?, ?, ?, ?, ?, ?)
                    """, (nome_paciente, idade, sexo, prediction, caminhobd, filename))
                    conn.commit()
                except sqlite3.IntegrityError:
                    print(f"Imagem {caminhobd} já existe no banco de dados. Pulando...")
            else:
                print(f"Paciente com imagem {caminhobd} já cadastrado. Pulando...")

            conn.close()
                
    flash('Imagens processadas e pacientes atualizados!')
    return redirect(url_for('dashboard'))

@app.route('/remover_paciente/<int:id>', methods=['POST'])
def remover_paciente(id):
    # Conectar ao banco de dados principal
    conn_pacientes = get_db_connection_pacientes()
    cursor_pacientes = conn_pacientes.cursor()

    # Buscar o paciente pelo ID
    cursor_pacientes.execute("SELECT * FROM pacientes WHERE id = ?", (id,))
    paciente = cursor_pacientes.fetchone()

    if paciente:
        # Conectar ao banco de dados de pacientes removidos
        conn_removidos = get_db_connection_removidos()
        cursor_removidos = conn_removidos.cursor()

        # Inserir o paciente no banco de dados de removidos
        cursor_removidos.execute("""
            INSERT INTO pacientes_removidos (patient_name, idade, sexo, diagnostico, caminho_imagem)
            VALUES (?, ?, ?, ?, ?)
        """, (paciente['patient_name'], paciente['idade'], paciente['sexo'], paciente['diagnostico'], paciente['caminho_imagem']))
        conn_removidos.commit()

        # Remover o paciente do banco de dados principal
        cursor_pacientes.execute("DELETE FROM pacientes WHERE id = ?", (id,))
        conn_pacientes.commit()

        # Fechar conexões
        conn_pacientes.close()
        conn_removidos.close()

    return redirect(url_for('dashboard'))

# Função para conectar ao banco de dados de pacientes removidos (pacientes_removidos.db)
def get_db_connection_removidos():
    conn = sqlite3.connect('pacientes_removidos.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_db_connection_pacientes():
    conn = sqlite3.connect('pacientes.db')  # Troquei users.db para pacientes.db
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/dashboard')
def dashboard():
    conn = get_db_connection_pacientes()
    # Modificando a consulta SQL para ordenar os pacientes de forma decrescente pelo diagnóstico
    pacientes = conn.execute("SELECT * FROM pacientes ORDER BY diagnostico DESC").fetchall()
    # Separar pacientes de alta prioridade
    alta_prioridade = []
    outros_pacientes = []
    
    for paciente in pacientes:
        try:
            valor = float(paciente['diagnostico'])
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

    conn = get_db_connection_pacientes()
    cursor = conn.cursor()

    # Buscar o paciente pelo ID
    cursor.execute("SELECT * FROM pacientes WHERE id = ?", (id,))
    paciente = cursor.fetchone()

    conn.close()

    # Se o paciente não existir, redireciona para o dashboard
    if not paciente:
        flash("Paciente não encontrado!", "error")
        return redirect(url_for('dashboard'))

    # Renderiza o template com os dados do paciente
    return render_template('detalhe.html', paciente=paciente)
    

if __name__ == '__main__':
    app.run(debug=True)

   
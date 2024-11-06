def predict():

    
    import sqlite3
    import numpy as np
    from tkinter import Tk
    from tkinter.filedialog import askopenfilename
    import imageio
    import cv2
    import pydicom
    import pandas as pd
    from tensorflow.keras.models import Sequential
    from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
    from tensorflow.keras.regularizers import l2
    import tensorflow as tf
    import os


    Tk().withdraw()
    file = askopenfilename()
    ds = pydicom.dcmread(file)

    # Função para converter DICOM para PNG
    def convert_to_png(file):
        ds = pydicom.dcmread(file)
        print(ds)
        image_2d = ds.pixel_array.astype(float)
        image_2d_scaled = (np.maximum(image_2d, 0) / image_2d.max()) * 255.0
        image_2d_scaled = np.uint8(image_2d_scaled)
        png_file_path = os.path.join('static/uploads', f'{os.path.basename(file).rstrip(".dcm")}.png')
        imageio.imwrite(png_file_path, image_2d_scaled)

        try:
            imageio.imwrite(png_file_path, image_2d_scaled)
            print(f'Successfully saved PNG to {png_file_path}')
        except Exception as e:
            print(f'Failed to save PNG: {e}')
        return png_file_path

    # Converter DICOM para PNG e carregar a imagem
    png_file_path = convert_to_png(file)
    image = cv2.imread(png_file_path)
    image = cv2.resize(image, (100, 100))

    # Exibir imagem
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    try:
        # Definir a arquitetura do modelo
        classificador = Sequential([
            Conv2D(32, 3, input_shape=(100, 100, 3), activation='relu'),
            MaxPooling2D(),
            Conv2D(16, 3, activation='relu'),
            MaxPooling2D(),
            Conv2D(16, 3, activation='relu'),
            MaxPooling2D(),
            Flatten(),
            Dense(512, activation='relu', kernel_regularizer=l2(0.001)),
            Dropout(0.5),
            Dense(256, activation='relu', kernel_regularizer=l2(0.001)),
            Dropout(0.5),
            Dense(1, activation='sigmoid')
        ])

        # Carregar o modelo sem a configuração de perda original
        classificador.load_weights(r"C:\Users\alice\Downloads\CNN_RaioX_COVID.weights.h5")
        
        # Recompilar o modelo com uma função de perda válida
        classificador.compile(optimizer='adam', loss=tf.keras.losses.BinaryCrossentropy(),
                              metrics=['accuracy'])
    except ValueError as e:
        print(f"Error loading model: {e}")

    # Fazer a previsão
    y_teste = classificador.predict(np.expand_dims(image, axis=0))  # Expandir a dimensão para o batch
    y_pred_binary = (y_teste > 0.5).astype(int).flatten()

    # Salvar no banco de dados
    paciente_id = ds.PatientID
    nome_paciente = " "
    idade = ds.PatientAge
    sexo = ds.PatientSex
    diagnostico = "COM COVID" if y_pred_binary == 1 else "SEM COVID"

    conexao = sqlite3.connect('pacientes.db')
    cursor = conexao.cursor()
    cursor.execute('''INSERT INTO pacientes (id, nome, diagnostico, idade, sexo, link)
                      VALUES (?, ?, ?, ?, ?, ?)''', 
                   (paciente_id, nome_paciente, diagnostico, idade, sexo, png_file_path))
    conexao.commit()
    conexao.close()

    print(f"Dados salvos no banco de dados para o paciente {nome_paciente}.")
    return y_pred_binary

predict()


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


def convert_to_png(file):
    # Função para converter DICOM para PNG
    ds = pydicom.dcmread(file)
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

    image = cv2.imread(png_file_path)
    image = cv2.resize(image, (100, 100))
    return image

#Classe do modelo de precição
class Modelo:
    def __init__(self, patch_peso):
        self.model = None
        # Definir a arquitetura do modelo
        self.model = Sequential([
            Conv2D(32, (3,3), input_shape=(100, 100, 3), activation='relu'),
            MaxPooling2D(),
            Conv2D(16, (3,3), activation='relu'),
            MaxPooling2D(),
            Conv2D(16, (3,3), activation='relu'),
            MaxPooling2D(),
            Flatten(),
            Dense(512, activation='relu', kernel_regularizer=l2(0.001)),
            Dropout(0.5),
            Dense(256, activation='relu', kernel_regularizer=l2(0.001)),
            Dropout(0.5),
            Dense(1, activation='sigmoid')
        ])


        
        # Recompilar o modelo com uma função de perda válida
        self.model.compile(optimizer='adam', loss=tf.keras.losses.BinaryCrossentropy(),
                                metrics=['accuracy']) 
        # Carregar o modelo sem a configuração de perda original
        #self.model.load_weights(patch_peso)

    def predict(self, file):
        #verifica se o arquivo é um DICOM ou png, caso seja DICOM, converte para png
        if file.endswith('.dcm'):
            file = convert_to_png(file)
        else:
            file = cv2.imread(file)

        #redimensiona a imagem para 100x100
        file = cv2.resize(file, (100, 100))

        #faz a previsão
        y_teste = self.model.predict(np.expand_dims(file, axis=0))
        #retorna 0 ou 1
        y_pred_binary = (y_teste > 0.5).astype(int).flatten()
        #retorna a previsão
        return y_pred_binary


if __name__ == "__main__":
    
    modelo = Modelo(r"C:\Users\alice\Downloads\1-1.dcm")
    print(modelo.predict(r"C:\Users\alice\Downloads\1-1.png"))
    print("finalizado")
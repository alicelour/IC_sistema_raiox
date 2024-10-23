def predict():
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

    Tk().withdraw()
    file = askopenfilename()
    ds = pydicom.dcmread(file)

    # Função para converter DICOM para PNG
    def convert_to_png(file):
        ds = pydicom.dcmread(file)
        image_2d = ds.pixel_array.astype(float)
        image_2d_scaled = (np.maximum(image_2d, 0) / image_2d.max()) * 255.0
        image_2d_scaled = np.uint8(image_2d_scaled)
        png_file_path = f'{file.rstrip(".dcm")}.png'
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
    cv2.imshow('DICOM to PNG', image)
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

    # Exibir a previsão
    redondo = np.round(y_teste, 2)
    print(f"Predição arredondada: {redondo}")
    print(f"Classificação binária: {y_pred_binary}")

    # Criar o DataFrame com os resultados
    output_df = pd.DataFrame({'id': 1, 'classe': y_pred_binary})
    print(output_df.head())

    # Salvar os resultados em um arquivo CSV
    output_df.to_csv("submission.csv", index=False)

    return y_pred_binary

predict()

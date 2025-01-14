# Bibliotecas principais
import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder, Normalizer
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Flatten
from tensorflow.keras.metrics import AUC
from collections import Counter
import seaborn as sns
import matplotlib.pyplot as plt
import tensorflow
import tensorflow.keras as keras
import cv2

def predict(image_path,feature_extractor_path, model_path):
    feature_extractor = keras.models.load_model(feature_extractor_path)
    model = keras.models.load_model(model_path)
    image = cv2.imread(image_path)
    image = cv2.resize(image, (224, 224))
    image = image / 255.0
    image = np.expand_dims(image, axis=0)
    features = feature_extractor.predict(image)
    prediction = model.predict(features)
    return prediction[0][0]

resultado= predict(r"C:\Users\alice\inv_u_binary\0\00000011_004.png", 'feature_extractor.h5', 'fuzzy_model.h5')
print(resultado)
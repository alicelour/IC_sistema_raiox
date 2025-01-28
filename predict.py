import os
import cv2
import numpy as np
import tensorflow.keras as keras

class ImagePredictor:
    def __init__(self, feature_extractor_path, model_path):
        self.feature_extractor = keras.models.load_model(feature_extractor_path)
        self.model = keras.models.load_model(model_path)

    def predict_image(self, image_path):
        image = cv2.imread(image_path)
        image = cv2.resize(image, (224, 224))
        image = image / 255.0
        image = np.expand_dims(image, axis=0)
        features = self.feature_extractor.predict(image)
        prediction = self.model.predict(features)
        
        return prediction[0][0]
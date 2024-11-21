import cv2
import numpy as np
from keras.applications.resnet import preprocess_input
from tensorflow.keras.models import load_model
import json
from config import LABEL_CLASSES_PATH, MODEL_PATH

class ClassificationModel:
    IMAGE_DIMS = (60, 60, 3)
    def __init__(self):
        print("====== Initializing Model ======")
        self.model = load_model(MODEL_PATH)
        self.labels = self._load_labels()

    def _load_labels(self):
        with open(LABEL_CLASSES_PATH, "r") as file:
            return json.load(file)

    def load_image(self, image_path):
        image = cv2.imread(image_path)
        image = cv2.resize(image, (self.IMAGE_DIMS[1], self.IMAGE_DIMS[0]))
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        return preprocess_input(image)        

    def predict(self, image_path):
        print("====== Load Image ======")
        image = self.load_image(image_path)
        image_data = np.expand_dims(image, axis=0)

        print("====== Predict ======")
        (subCategoryProba, articleProba, genderProba, colorProba, seasonProba, usageProba) = self.model.predict(image_data)

        subCategoryIdx = subCategoryProba[0].argmax()
        articleIdx = articleProba[0].argmax()
        genderIdx = genderProba[0].argmax()
        colorIdx = colorProba[0].argmax()
        seasonIdx = seasonProba[0].argmax()
        usageIdx = usageProba[0].argmax()

        subCategoryLabel = self.labels["subCategory"][subCategoryIdx]
        articleLabel = self.labels["articleType"][articleIdx]
        genderLabel = self.labels["gender"][genderIdx]
        colorLabel = self.labels["baseColour"][colorIdx]
        seasonLabel = self.labels["season"][seasonIdx]
        usageLabel = self.labels["usage"][usageIdx]

        return {
            "subCategory": subCategoryLabel,
            "articleType": articleLabel,
            "gender": genderLabel,
            "baseColour": colorLabel,
            "season": seasonLabel,
            "usage": usageLabel
        }
import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '1'
import cv2
import json
from keras.applications.resnet import preprocess_input
from tensorflow.keras.models import Model
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.layers import Input, Flatten, Dense, Activation
import tensorflow as tf
import numpy as np
from tensorflow.keras.models import load_model

LABEL_CLASSES_PATH = "model/label_classes.json"
MODEL_PATH = "model/clothes_classifier.h5"
DATA_PATH = "test/"
CLASSES_PATH = "/clothes_categories/classes.txt"
IMAGE_DIMS = (60, 60, 3)

with open(LABEL_CLASSES_PATH, "r") as json_file:
    LABEL_CLASSES = json.load(json_file)

def make_branch(res_input, n_out, act_type, name):
    z = Dense(512, activation="relu")(res_input)
    z = Dense(256, activation='relu')(z)
    z = Dense(128, activation='relu')(z)
    z = Dense(n_out)(z)
    z = Activation(act_type, name=name+'_output')(z)
    return z

def build_model():
    weight_init = "model/resnet50_weights_tf_dim_ordering_tf_kernels_notop.h5"
    # -------------------------
    res50 = ResNet50(weights=weight_init, include_top=False, input_shape=IMAGE_DIMS)
    res50.trainable=False
    inputs = Input(shape=IMAGE_DIMS)
    x = res50(inputs, training=False)
    x = Flatten()(x)
    x = Dense(1024, activation='relu')(x)
    # -------------------------
    sub_category_branch = make_branch(x, len(LABEL_CLASSES["subCategory"]), 'softmax', 'subCategory')
    article_branch = make_branch(x, len(LABEL_CLASSES["articleType"]), 'softmax', 'article')
    gender_branch = make_branch(x, len(LABEL_CLASSES["gender"]), 'softmax', 'gender')
    color_branch = make_branch(x, len(LABEL_CLASSES["baseColour"]), 'softmax', 'color')
    season_branch = make_branch(x, len(LABEL_CLASSES["season"]), 'softmax', 'season')
    usage_branch = make_branch(x, len(LABEL_CLASSES["usage"]), 'softmax', 'usage')

    model = Model(inputs=inputs,
                outputs=[sub_category_branch, article_branch, gender_branch, color_branch, 
                            season_branch, usage_branch])
    return model

class ClassificationModel():
    
    def __init__(self):
        print("====== Initializing Model ======")
        # Load the dictionary from the JSON file
        
    
    def load_image(self, image_path):
        image = cv2.imread(image_path)
        image = cv2.resize(image, (IMAGE_DIMS[1], IMAGE_DIMS[0]))
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = preprocess_input(image)
        return image

    def load(self, model_path):
        print("====== Loading Model ======")
        print(model_path)
        self.model = load_model(model_path)
    
    def predict(self, image_path):
        print("====== Load image ======")
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

        subCategoryLabel = LABEL_CLASSES["subCategory"][subCategoryIdx]
        articleLabel = LABEL_CLASSES["articleType"][articleIdx]
        genderLabel = LABEL_CLASSES["gender"][genderIdx]
        colorLabel = LABEL_CLASSES["baseColour"][colorIdx]
        seasonLabel = LABEL_CLASSES["season"][seasonIdx]
        usageLabel = LABEL_CLASSES["usage"][usageIdx]


        return {
            "subCategory": subCategoryLabel,
            "articleType": articleLabel,
            "gender": genderLabel,
            "baseColour": colorLabel,
            "season": seasonLabel,
            "usage": usageLabel
        }

# print(tf.__version__)
learner = ClassificationModel()
learner.load(MODEL_PATH)
print(DATA_PATH+"1.jpg")
output = learner.predict(DATA_PATH+"1.jpg")
print(output)
from tensorflow.keras.models import load_model
import numpy as np
from PIL import Image
import os

cur_dir = os.path.abspath(os.path.dirname(__file__))

model = load_model(os.path.join(cur_dir,"model.h5"))
classes = ["Cats","KanyeWest","Pikachu"]


import matplotlib.pyplot as plt

def predict(image_path):

    image = Image.open(image_path).convert('RGB')
    # scale
    width, height = image.size
    if min(width,height)>256:
        image.thumbnail((256,256), Image.ANTIALIAS)
    else:
        factor = min(width,height)/256
        new_width,new_height = int(width/factor),int(height/factor)
        image.thumbnail((new_width,new_height), Image.ANTIALIAS)


    # crop
    new_width, new_height = 256,256
    width, height = image.size   # Get dimensions
    left = (width - new_width)/2
    top = (height - new_height)/2
    right = (width + new_width)/2
    bottom = (height + new_height)/2
    image = image.crop((left, top, right, bottom))

    image = np.array(image)
    image = image/255

    image = image.reshape(1,256,256,3)

    preds = model.predict(image)[0]
    print("Predictions :",preds)

    return classes[np.argmax(preds)]
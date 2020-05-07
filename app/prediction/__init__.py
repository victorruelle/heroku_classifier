# from tensorflow.keras.models import load_model
import tflite_runtime.interpreter as tflite
from flask import url_for
import numpy as np
from PIL import Image
import os

from app import app

classes = ["Cats","KanyeWest","Pikachu"]

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
    image = np.float32(image)
    
    interpreter = tflite.Interpreter(model_path=os.path.join(app.static_folder,"model.tflite"))
    interpreter.allocate_tensors()

    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()


    interpreter.set_tensor(input_details[0]['index'], image)
    interpreter.invoke()
    output_data = interpreter.get_tensor(output_details[0]['index'])

    preds = np.squeeze(output_data)

    return classes[np.argmax(preds)]
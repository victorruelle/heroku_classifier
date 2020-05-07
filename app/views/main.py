from flask import Blueprint, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import os
import numpy as np
import cv2

from app import app 

from app.prediction import predict

main = Blueprint('main', __name__)

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

ALLOWED_EXTENSIONS = {"jpg","jpeg","png"}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

predictions = {}

@main.route('/')
def index():
    return render_template("index.html", predictions=predictions)

    # content_type = 'image/jpeg'
    # headers = {'content-type': content_type}
    # response = requests.post(test_url, data=img_encoded.tostring(), headers=headers)

@main.route('/',methods=["GET",'POST'])
def index_post():
    if request.method == "POST":

        if request.files and "image" in request.files:

            image = request.files["image"]
            if allowed_file(image.filename):
                image_name = "input_{}.jpg".format(len(predictions))
                image_path = os.path.join(basedir,"static","images",image_name)
                image.save(image_path)
                prediction = predict(image_path)
                predictions[image_name]=prediction

            # return render_template("index.html",predictions=predictions)
            return render_template("index.html",predictions=predictions)

    # r = request
    # # convert string of image data to uint8
    # nparr = np.fromstring(r.data, np.uint8)
    # # decode image
    # img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    # prediction = model.predict.predict(img) 
    # render_template("index",prediction=prediction)
    
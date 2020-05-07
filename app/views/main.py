from flask import Blueprint, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import os
import numpy as np

from app import app 

from app.prediction import predict

main = Blueprint('main', __name__)

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

ALLOWED_EXTENSIONS = {"jpg","jpeg","png"}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

predictions = []
image_names = []

@main.route('/')
def index():
    return render_template("index.html",image_names=image_names,predictions=predictions)


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
                predictions.insert(0,prediction)
                image_names.insert(0,image_name)

            return render_template("index.html",image_names=image_names,predictions=predictions)
    
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

class History():

    def __init__(self):
        self.predictions = []
        self.image_names = []

history = History()

@main.route('/')
def index():
    return render_template("index.html",image_names=history.image_names,predictions=history.predictions)


@main.route('/',methods=["GET",'POST'])
def index_post():
    if request.method == "POST":

        if request.files and "image" in request.files:

            image = request.files["image"]
            if allowed_file(image.filename):
                image_name = "input_{}.jpg".format(len(history.predictions))
                image_path = os.path.join(basedir,"static","images",image_name)
                image.save(image_path)
                prediction = predict(image_path)
                history.predictions.insert(0,prediction)
                history.image_names.insert(0,image_name)

            return render_template("index.html",image_names=history.image_names,predictions=history.predictions)


@main.route('/refresh')
def refresh():
    for image_name in history.image_names:
        image_path = os.path.join(basedir,"static","images",image_name)
        try:
            os.remove(image_path)
        except Exception:
            print("ERROR : could not delete image {}".format(image_path))
        history.image_names = []
        history.predictions = []
    
    return redirect(url_for("main.index"))
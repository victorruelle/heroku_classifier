from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
import os
import numpy as np
import requests

from app import app
from app.prediction import predict
from app.data import data_manager, get_session_id

main = Blueprint('main', __name__)

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png"}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@main.route('/')
def index():
    print("session id is", get_session_id())
    return render_template("index.html", image_name=data_manager.get_image_name(), prediction=data_manager.get_prediction())


@main.route('/', methods=["GET", 'POST'])
def index_post():

    try:
        if request.method == "POST":

            if request.files and "image" in request.files:

                image = request.files["image"]
                if allowed_file(image.filename):
                    session_id = get_session_id()
                    data_manager.init_user(session_id)
                    image_name = "{}_input.jpg".format(session_id)
                    image_path = os.path.join(
                        basedir, "static", "images", image_name)
                    image.save(image_path)
                    prediction = predict(image_path)
                    data_manager.record(image_name, prediction)

                return render_template("index.html", image_name=data_manager.get_image_name(), prediction=data_manager.get_prediction())

            # test for url
            elif request.form and "url" in request.form:
                url = request.form.get("url")
                session_id = get_session_id()
                data_manager.init_user(session_id)
                image_name = "{}_input.jpg".format(session_id)
                image_path = os.path.join(basedir, "static", "images", image_name)
                print("Downloading url {}".format(url))

                try:
                    response = requests.get(url)
                    with open(image_path,"wb") as output:
                        output.write(response.content)
                except Exception:
                    print("ERROR : could not load image")
                    flash("Could not load image, please try again with another one!")
                    return render_template("index.html", image_name=data_manager.get_image_name(), prediction=data_manager.get_prediction())
                
                prediction = predict(image_path)
                data_manager.record(image_name, prediction)

                return render_template("index.html", image_name=data_manager.get_image_name(), prediction=data_manager.get_prediction())
            
            else:
                raise Exception("Unexpected request : {}".format(request))
    
    except Exception as err:
        print("Caught unexpected error... starting over")
        flash("Caught unexpected error {}... starting over".fomat(err))
        data_manager.refresh()
        return render_template("index.html", image_name=data_manager.get_image_name(), prediction=data_manager.get_prediction())


@main.route('/refresh')
def refresh():
    data_manager.remove_user(get_session_id())
    return redirect(url_for("main.index"))

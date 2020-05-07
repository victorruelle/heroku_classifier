from flask import Blueprint, render_template, request, redirect, url_for, session
from werkzeug.utils import secure_filename
import os
import numpy as np
import time

from app import app 

from app.prediction import predict

main = Blueprint('main', __name__)

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

ALLOWED_EXTENSIONS = {"jpg","jpeg","png"}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_session_id():
    return session['_id']

class History():

    DATA_PERSISTANCE = 600

    def __init__(self):
        self.predictions = {}
        self.image_names = {}
        self.history = {}
    
    def init_user(self):
        self.remove_old_users()
        session_id = get_session_id()
        self.predictions[session_id] = []
        self.image_names[session_id] = []
        self.history[session_id] = time.time()

    def exists(self):
        return get_session_id() in self.history

    def add_record(self,image_name,prediction):
        self.remove_old_users()
        session_id = get_session_id()
        if not self.exists():
            self.init_user(session_id)
        self.predictions[session_id].insert(0,prediction)
        self.image_names[session_id].insert(0,image_name)
    
    def get_predictions(self):
        self.remove_old_users()
        session_id = get_session_id()
        if not self.exists():
            self.init_user(session_id)
        return  self.predictions[session_id]

    def get_image_names(self):
        self.remove_old_users()
        session_id = get_session_id()
        if not session_id in self.image_names:
            self.init_user(session_id)
        return  self.image_names[session_id]

    def remove_user(self,session_id):

        for image_name in self.image_names[session_id]:
            image_path = os.path.join(basedir,"static","images",image_name)
            try:
                os.remove(image_path)
            except Exception:
                print("ERROR : could not delete image {}".format(image_path))
        
        if session_id in self.predictions:
            self.predictions.pop(session_id)
        if session_id in self.image_names:
            self.image_names.pop(session_id)
        if session_id in self.history:
            self.history.pop(session_id)

    def remove_old_users(self):
        now = time.time()
        for session_id in self.history:
            if now - self.history[session_id] > History.DATA_PERSISTANCE :
                self.remove_user(session_id)
    
history = History()

@main.route('/')
def index():
    print("Session object is",session)
    print(dict(session))
    return render_template("index.html",image_names=history.image_names,predictions=history.predictions)


@main.route('/',methods=["GET",'POST'])
def index_post():
    if request.method == "POST":

        if request.files and "image" in request.files:

            image = request.files["image"]
            if allowed_file(image.filename):
                session_id = get_session_id()
                image_name = "{}_input_{}.jpg".format(session_id,len(history.get_predictions()))
                image_path = os.path.join(basedir,"static","images",image_name)
                image.save(image_path)
                prediction = predict(image_path)
                history.add_record(image_name,prediction)

            return render_template("index.html",image_names=history.get_image_names(),predictions=history.get_predictions())


@main.route('/refresh')
def refresh():
    history.remove_old_users(get_session_id())
    return redirect(url_for("main.index"))
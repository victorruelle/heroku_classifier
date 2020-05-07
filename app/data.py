from flask import request, url_for
import time
import os

from app import app

def get_session_id():
    return request.remote_addr
    # return session['_id']

class DataManager():

    DATA_PERSISTANCE = 120

    def __init__(self):
        self.predictions = {}
        self.image_names = {}
        self.history = {}
    
    def init_user(self,session_id=None):
        self.remove_old_users()
        session_id = session_id or get_session_id()
        self.predictions[session_id] = ""
        self.image_names[session_id] = ""
        self.history[session_id] = time.time()

    def exists(self,session_id = None):
        session_id = session_id or get_session_id()
        return session_id in self.image_names

    def record(self,image_name,prediction):
        self.remove_old_users()
        session_id = get_session_id()
        if not self.exists():
            self.init_user()
        self.predictions[session_id] = prediction
        self.image_names[session_id] = image_name
    
    def get_prediction(self):
        self.remove_old_users()
        if not self.exists():
            self.init_user()
        session_id = get_session_id()
        return  self.predictions[session_id]

    def get_image_name(self):
        self.remove_old_users()
        if not self.exists():
            self.init_user()
        session_id = get_session_id()
        return  self.image_names[session_id]

    def remove_user(self,session_id):
        if self.exists(session_id):
            assert session_id in self.image_names, "{} does not contain {}".format(self.image_names,session_id)
            image_name = self.image_names[session_id]
            image_path = os.path.join(app.static_folder,"images",image_name)
            try:
                os.remove(image_path)
            except Exception:
                print("ERROR : could not delete image {}".format(image_path))            
            self.predictions.pop(session_id)
            self.image_names.pop(session_id)
        else:
            pass

    def remove_old_users(self):
        now = time.time()
        for session_id in self.history:
            if self.exists(session_id) and now - self.history[session_id] > DataManager.DATA_PERSISTANCE :
                self.remove_user(session_id)

    def refresh(self):
        self.predictions = {}
        self.image_names = {}
        self.history = {}

    
data_manager = DataManager()
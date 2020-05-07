from flask import request
import time
import os

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

def get_session_id():
    return request.remote_addr
    # return session['_id']

class DataManager():

    DATA_PERSISTANCE = 600

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
        return session_id in self.history

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
        print("Getting predictions for {} : {} in {}".format(self.predictions[session_id],session_id,self.predictions))
        return  self.predictions[session_id]

    def get_image_name(self):
        self.remove_old_users()
        if not self.exists():
            self.init_user()
        session_id = get_session_id()
        print("Getting image names for {} : {} in  {}".format(session_id,self.image_names[session_id],self.image_names))
        return  self.image_names[session_id]

    def remove_user(self,session_id):
        if self.exists(session_id):
            assert session_id in self.image_names, "{} does not contain {}".format(self.image_names,session_id)
            image_name = self.image_names[session_id]
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
        else:
            pass

    def remove_old_users(self):
        now = time.time()
        for session_id in self.history:
            if now - self.history[session_id] > DataManager.DATA_PERSISTANCE :
                self.remove_user(session_id)
    
data_manager = DataManager()
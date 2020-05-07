from flask import Flask
import os

app = Flask(__name__)
# app.config.from_object('config')
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

from app import routes

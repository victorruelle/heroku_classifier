from flask import Flask
import os

app = Flask(__name__)
app.config.from_object('config')
app.config['UPLOAD_FOLDER'] = os.path.join("static","images")


# blueprint for non-auth parts of app
from app.views.main import main as main_blueprint
app.register_blueprint(main_blueprint)


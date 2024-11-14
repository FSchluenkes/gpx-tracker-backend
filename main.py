from flask import Flask, jsonify, request
import os
from extensions import db
import models
from blueprints.upload import upload_bp
from blueprints.tracks import tracks_bp
from flask_cors import CORS

def create_app():
  app = Flask(__name__)
  CORS(app)
  app.config.from_prefixed_env()

  if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])
    
  db.init_app(app)
  
  with app.app_context():
    #db.drop_all()
    db.create_all()

  app.register_blueprint(upload_bp, url_prefix='/upload')
  app.register_blueprint(tracks_bp, url_prefix='/get_tracks')
  

  return app
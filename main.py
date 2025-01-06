from flask import Flask
import os
from extensions import db
import models
from blueprints.upload import upload_bp
from blueprints.tracks import tracks_bp
from blueprints.stats import stats_bp
from blueprints.path import path_bp
from blueprints.graph import graph_bp
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
  app.register_blueprint(stats_bp, url_prefix='/get_stats')
  app.register_blueprint(path_bp, url_prefix='/get_path')
  app.register_blueprint(graph_bp, url_prefix='/get_graph')
  

  return app
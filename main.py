from flask import Flask
from extensions import db
import models

def create_app():
  app = Flask(__name__)
    
  app.config.from_prefixed_env()
    
  db.init_app(app)
  
  with app.app_context():
    #db.drop_all()
    db.create_all()

  return app
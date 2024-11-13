from flask import Flask
from backend.database import db

app = None

def create_app():
  app = Flask(__name__)
  app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hss.sqlite3'
  db.init_app(app)
  app.debug = True
  app.app_context().push()
  return app

app = create_app()

from backend.controllers import *
from backend.customerController import *
from backend.adminController import *
from backend.professionalController import *

if __name__ == "__main__":
  app.run()
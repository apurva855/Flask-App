from flask import Flask
#from flask_mysqldb import MySQL
import pymysql
from flask_sqlalchemy import SQLAlchemy
#from mysqlsampledatabase.sql import text
from sqlalchemy.ext.automap import automap_base
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from apurva_flask_app.config import DevelopmentConfig

app = Flask(__name__)
app.config.from_object(DevelopmentConfig())

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager= LoginManager(app)

Base = automap_base()
Base.prepare(db.engine,reflect=True)

from apurva_flask_app import routes
#from apurva_flask_app import app

class Config(object):
    TESTING = False
    
class ProductionConfig(Config):
     pass

class DevelopmentConfig(Config):
    DEBUG = True
    SECRET_KEY= 'cc5735479b1360a55266eae28ec7a415'
    SQLALCHEMY_DATABASE_URI= 'mysql+pymysql://debian-sys-maint:8dJJzZ2IFgM0vCM2@localhost/classicmodels'
    SQLALCHEMY_TRACK_MODIFICATIONS= True

class TestingConfig(Config):
    TESTING = True
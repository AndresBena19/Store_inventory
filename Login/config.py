import os

class Config(object):
    SECRET_KEY= 'KEY'

class DBconfig(Config):
    DEBUG =True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database/DB.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

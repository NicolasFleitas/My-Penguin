import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    #solo para desarrollo, luego cambiar la clave 
    SECRET_KEY = 'esta-es-mi-clave-secreta' 
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

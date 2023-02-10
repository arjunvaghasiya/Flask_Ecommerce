from flask import Flask
from datetime import timedelta
from flask_jwt_extended import JWTManager
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_mail import Mail,Message
from .create_database import create_database
from .models import db
create_database()
app =  Flask(__name__)
api = Api(app)
db.init_app(app)
app.config['SECRET_KEY'] = 'f19dg6n719d04f6bdg7867h1wee8ju7l1y9ugykm1nmkhgOPUJHN86753DRdrt'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:abc123@localhost/ecommerce'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['JWT_SECRET_KEY'] = 'JWT_SECRET_KEY'
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=9)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(minutes=10)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = "arjunvaghasiya361@gmail.com"
app.config['MAIL_PASSWORD'] = "jupxfdgokubxbpgm"
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['FROM_EMAIL'] = "arjunvaghasiya361@gmail.com"


migrate = Migrate(app,db)
ma = Marshmallow(app)
JWTManager(app)
mail = Mail(app)

from website import views


# {
#   "username":"user-9501",
#   "email":"proiruzeippipro-9501@yopmail.com",
#   "password":"abc123",
#   "password_verify":"abc123",
#   "first_name": "proiru",
#   "last_name": "pipro",
#   "gender": "Male",
#   "age": "45",
#   "address": "Rajkot",
#   "phone": "9698785623"
#   }
from flask import Flask,render_template
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from os import environ
from flask_openid import OpenID
import os
from flask_cors import CORS
from flask_login import LoginManager,login_user, logout_user, current_user, login_required,UserMixin

#иницилиазация приложения
app = Flask(__name__)

#login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
app.secret_key = 'lilpenis'

#заголовки
CORS(app)

#база данных
db = SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///goods.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'sad'
app.config['EXTEND_EXISTING'] = True


#admin







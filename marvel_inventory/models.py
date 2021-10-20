from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import uuid
from datetime import datetime
from sqlalchemy.orm import backref
from werkzeug.security import generate_password_hash, check_password_hash

from flask_login import UserMixin


from flask_login import LoginManager


from flask_marshmallow import Marshmallow

import secrets


db = SQLAlchemy()
login_manager = LoginManager()
ma = Marshmallow()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    id = db.Column(db.String(150), primary_key = True)
    first_name = db.Column(db.String(150), nullable = True, default = '')
    last_name = db.Column(db.String(150), nullable = True, default = '')
    email = db.Column(db.String(150), nullable = False)
    password = db.Column(db.String(150), nullable = True)
    token =db.Column(db.String, default='', unique= True)
    date_created = db.Column(db.DateTime, nullable = False, default= datetime.utcnow)
    character = db.relationship('Character', backref='owner', lazy=True)

    def __init__(self, email, first_name='', last_name='', id='', password='',token=''):
        self.id= self.set_id()
        self.first_name= first_name
        self.last_name= last_name
        self.password= self.set_password(password)
        self.email= email
        self.token= self.set_token(24)
        

    def set_token(self, length):
        return secrets.token_hex(length)

    def set_id(self):
        return str(uuid.uuid4())

    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)
        return self.pw_hash

    def __repr__(self):
        return f'User {self.email} has been added to the database.'

class Character(db.Model):
    id = db.Column(db.String, primary_key = True)
    name = db.Column(db.String(150))
    description = db.Column(db.String(200), nullable = True)
    cosmics_appeared_in = db.Column(db.String(100))
    super_power = db.Column(db.String(100))
    user_token = db.Column(db.String, db.ForeignKey('user.token'), nullable = False)

    def __init__(self,name,description,cosmics_appeared_in,super_power,user_token, id = ''):
        self.id = self.set_id()
        self.name = name
        self.description = description
        self.cosmics_appeared_in = cosmics_appeared_in
        self.super_power = super_power
        self.user_token = user_token


    def __repr__(self):
        return f'The following Car has been added: {self.name}'

    def set_id(self):
        return (secrets.token_urlsafe())



class CharacterSchema(ma.Schema):
    class Meta:
        fields = ['id', 'name','description', 'cosmics_appeared_in', 'super_power']


character_schema = CharacterSchema()
characters_schema = CharacterSchema(many = True)
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_login import UserMixin
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine, inspect
import base64


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.sqlite3'

db = SQLAlchemy(app)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

engine = create_engine('sqlite:///test.sqlite3')
insp = inspect(engine)
table_names = insp.get_table_names() 



class User(UserMixin, db.Model):
    __tablename__ = 'UserInfo'
    id = db.Column(db.Integer, primary_key=True)
    Username = db.Column(db.String(20), unique=True, nullable=False)
    Password = db.Column(db.String(16), nullable=False)  
    # User_avatar = db.relationship("User_avatar", backref='User')
    Image_id = db.Column(db.Integer, nullable=False)
    
    def __init__(self, Password, Username, Image_id):
        self.Password = Password
        self.Username = Username
        self.Image_id = Image_id


# class User_avatar(db.Model):
#     __tablename__ = 'User_avatar'
#     id = db.Column(db.Integer, primary_key=True)
#     User_id = db.Column(db.Integer, db.ForeignKey('UserInfo.id'))
#     Image_id = db.Column(db.String(), nullable=True)
    # def __init__(self, User_id, Image):
    #     self.User_id = User_id
    #     self.Image = Image




class Global_msgs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Message = db.Column(db.String())
    
    def __init__(self, Message):
        self.Message = Message

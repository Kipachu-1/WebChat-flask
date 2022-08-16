from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_login import UserMixin

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.sqlite3'
db = SQLAlchemy(app)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Username = db.Column(db.String(80), unique=True, nullable=False)
    Password = db.Column(db.String(120),nullable=False)  
    
    
    def __init__(self, Password, Username):
        self.Password = Password
        self.Username = Username
        

class Global_msgs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Message = db.Column(db.String())
    
    def __init__(self, Message):
        self.Message = Message



# new_user1 = User(Username='Aipachu', Password='230279mm')
# new_user2 = User(Username='Kipachu', Password='230279mm')

# # print(User.query.filter_by(Username='Kipacho').all())
# db.session.add(new_user1)
# db.session.add(new_user2)
# db.session.commit()


# new_user = User(Username='Aipachu', Password='230279am')
# db.session.add(new_user)
# db.session.commit()


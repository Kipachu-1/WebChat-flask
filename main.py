from flask import Flask, request, render_template, url_for, redirect, flash, session
from flask_socketio import SocketIO, send, emit, join_room, leave_room
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_required, logout_user, login_user, UserMixin, current_user
from Base import *
from wtforms import StringField, PasswordField, SubmitField
from werkzeug.security import generate_password_hash, check_password_hash
import os


app = Flask(__name__)
app.secret_key = 'ajcinfuiehadiawd99481rr327982dj293'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL", 'sqlite:///test.sqlite3')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
socketio = SocketIO(app, cors_allowed_origins='*')
login_manager = LoginManager()
login_manager.init_app(app)
db.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Please login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@socketio.on('message')
def handle_message(message):
    msg = Global_msgs(Message=message)
    db.session.add(msg)
    db.session.commit()
    send(message=message, broadcast=True)

@socketio.on('message', namespace='/chat')
def handle_my_custom_event(message):
    send(message, broadcast=True)
    
@app.route('/chat')
def chat_page():
    return render_template('chat_page.html')



@app.route('/')
def intro_page():
    return render_template('intro_page.html')



@app.route('/login', methods = ['POST', 'GET'])
def login():
    if(request.method == 'POST'):
        Username = request.form.get('Username')
        Password = request.form.get('Password')
        try:
            user = User.query.filter_by(Username=f'{Username}').all()[0]
            if check_password_hash(user.Password, Password):
                login_user(user)
                try:
                    next = request.args.get('next')
                    return redirect(next)
                except:
                    return redirect(main_page)
            else:
                flash('Invalid email or password', 'warning')
        except:
            flash('The username no here', 'warning')
    return render_template('login_page2.html')


@app.route('/SignUp', methods=['POST', 'GET'])
def SignUp():
    if (request.method == "POST"):
        New_Username = request.form.get('UsernameS')
        Password1 = request.form.get('Password1')
        Password2 = request.form.get('Password2')
        check_db = User.query.filter_by(Username=New_Username).all()
        if Password1 == Password2 and check_db == []:
            Password_hash = generate_password_hash(Password1, method='pbkdf2:sha256', salt_length=20)
            New_User = User(Username=New_Username, Password=Password_hash)
            db.session.add(New_User)
            db.session.commit()
            return redirect('login')
        elif check_db != []:
            flash('Username is taken')
        elif Password1 != Password2:
            flash('Please check passwords')
        
    return render_template('SignUp_page.html')


# @app.route('/')
# def intro_page():
#     return render_template()




@app.route('/name')
@login_required
def name():
    return current_user.Password
       


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/login')

@app.route('/res', methods=['POST', 'GET'])
@login_required
def res_page():
    return render_template('assa.html')

@app.route('/ars', methods=['POST', 'GET'])
@login_required
def arse():
    return render_template('assa.html')

            
            
@app.route('/wrong')
def wrong():
    return 'wrong pass or username!'            
                  

@app.route('/home')
@login_required
def main_page():
    msgs = Global_msgs.query.all()
    name = current_user.Username
    return render_template('main_page.html', history_message=msgs, name=name)

if __name__ == '__main__':
    socketio.run(app, host='https://messenger-kipachu.herokuapp.com', debug=True)
    
    
    
    
    
    

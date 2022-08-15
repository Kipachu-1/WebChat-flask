from flask import Flask, request, render_template, url_for, redirect, flash, session
from flask_socketio import SocketIO, send
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_required, logout_user, login_user, UserMixin, current_user
from Base import *
from wtforms import StringField, PasswordField, SubmitField
link1 = 'https://www.onlinetutorialspoint.com/flask/python-flask-login-form-example.html'
link2 = 'https://iq.opengenus.org/login-page-in-flask/'

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.sqlite3'
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
    print('received message:' + message)
    if message != 'User Connected!':
        send(message=message, broadcast=True)



@app.route('/login', methods = ['POST', 'GET'])
def login():
    if(request.method == 'POST'):
        Username = request.form.get('Username')
        Password = request.form.get('Password')
        try:
            user = User.query.filter_by(Username=f'{Username}').all()[0]
            if Username == user.Username and Password == user.Password:
                login_user(user)
                next = request.args.get('next')
                return redirect(next)
            else:
                flash('Invalid email or password', 'warning')
        except:
            flash('Invalid email or password', 'warning')
    return render_template('login_page2.html')


@app.route('/SignUp', methods=['POST', 'GET'])
def SignUp():
    if (request.method == "POST"):
        New_Username = request.form.get('UsernameS')
        Password1 = request.form.get('Password1')
        Password2 = request.form.get('Password2')
        check_db = User.query.filter_by(Username=New_Username).all()
        if Password1 == Password2 and check_db == []:
            New_User = User(Username=New_Username, Password=Password1)
            db.session.add(New_User)
            db.session.commit()
            return redirect('login')
        elif check_db != []:
            flash('Username is taken')
        elif Password1 != Password2:
            flash('Please check passwords')
        
    return render_template('SignUp_page.html')


@app.route('/')
def intro_page():
    return render_template()




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


@app.route('/')
def smt():
    return 'it is the beginning, bro'
            
            
@app.route('/wrong')
def wrong():
    return 'wrong pass or username!'            
                  

@app.route('/home')
@login_required
def main_page():
    name = current_user.Username
    return render_template('main_page.html', name=name)

if __name__ == '__main__':
    socketio.run(app, host='172.20.10.2', debug=True)
    
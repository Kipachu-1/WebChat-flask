from distutils.log import debug
from flask import Flask, request, render_template, url_for, redirect, flash
from flask_socketio import SocketIO, send
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from Base import *


app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
socketio = SocketIO(app, cors_allowed_origins='*')
login_manager = LoginManager()
db.init_app(app)




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
            data = User.query.filter_by(Username=f'{Username}').all()[0]
            if Username == data.Username and Password == data.Password:
                return  redirect('/success')
            else:
                return redirect('/wrong')
        except:
            flash('Invalid email or password', 'warning')
        
    return render_template('login_page2.html')
            
            
@app.route('/wrong')
def wrong():
    return 'wrong pass or username!'            
            
@app.route('/success')
def success():
    return 'it is working!'       

@app.route('/')
def main_page():
    return render_template('main_page.html')

if __name__ == '__main__':
    socketio.run(app, host='172.20.10.2', debug=True)
    
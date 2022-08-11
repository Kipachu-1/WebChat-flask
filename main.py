from flask import Flask, request, render_template, url_for
from flask_socketio import SocketIO, send
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


db = SQLAlchemy()
app = Flask(__name__)
app.config['SECRET KEY'] = 'secret123'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
socketio = SocketIO(app, cors_allowed_origins='*')
login_manager = LoginManager()





@socketio.on('message')
def handle_message(message):
    print('received message:' + message)
    if message != 'User Connected!':
        send(message=message, broadcast=True)


@app.route('/login')
def login():
    return render_template('login_page.html')

@app.route('/')
def main_page():
    return render_template('main_page.html')

if __name__ == '__main__':
    socketio.run(app, host='172.20.10.2')
    
from flask import Flask, request, render_template, url_for
from flask_socketio import SocketIO, send


app = Flask(__name__)
app.config['SECRET KEY'] = 'secret123'

socketio = SocketIO(app, cors_allowed_origins='*')

@socketio.on('message')
def handle_message(message):
    print('received message:' + message)
    if message != 'User Connected!':
        send(message=message, broadcast=True)


@app.route('/')
def main_page():
    return render_template('main_page.html')

if __name__ == '__main__':
    socketio.run(app, host='localhost')
    
from flask import Flask, request, render_template, url_for, redirect, flash, abort
from flask_socketio import SocketIO, send
from flask_login import LoginManager, login_required, logout_user, login_user, current_user
from Base import *
from werkzeug.security import generate_password_hash, check_password_hash
import random
import os


app = Flask(__name__)
app.secret_key = 'hello'
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
    
def gene_chat_id(name):
    Users_block = User.query.all()
    list = []
    for i in Users_block:
        list2 = [i.Username, name]
        list2 = sorted(list2)
        uni_id = list2[0] + '_' + list2[1]
        dict1 = {
            'name' : i.Username,
            'uni_id': uni_id,
            'Image_id': str(i.Image_id)
        }
        list.append(dict1) 
    return list


@app.route('/')
def intro_page():
    return render_template('intro_page.html')

    
@app.route('/home')
@login_required
def main_page():
    msgs = Global_msgs.query.all()
    name = current_user.Username
    return render_template('main_page.html', chat_history=msgs, name=name, Users_block=gene_chat_id(name))


@app.route('/home/<chatid>')
@login_required
def room_page(chatid):
    name = current_user.Username
    
    if f"{chatid}" not in table_names:
        class Chat_id(db.Model):
            __table_args__ = {'extend_existing': True}
            __tablename__ = f'{chatid}'
            id = db.Column(db.Integer, primary_key=True)
            Message = db.Column(db.String(), nullable=False)
        try:
            Chat_id.__table__.create(db.session.bind)
        except: 
            pass
    chat_history = engine.connect().execute(f"SELECT Message FROM {chatid}") 
    @socketio.on('message',  namespace=f'/home/{chatid}')
    def handle_my_custom_event(message):
        engine.connect().execute(f'INSERT INTO {chatid} (Message) VALUES ("{message}")')
        send(message, broadcast=True)
    Cut_name = str(chatid).replace('_', '')
    Cut_name = Cut_name.replace(name, '')
    User_avatar = str(User.query.filter_by(Username=Cut_name).all()[0].Image_id)
    if name not in chatid:
        return abort(404)
    else:
        return render_template('chat_page.html', name=name, id=chatid, chat_history=chat_history,
                           Cut_name=Cut_name, Users_block=gene_chat_id(name), User_avatar=User_avatar)





@app.route('/login', methods = ['POST', 'GET'])
def login():
    if(request.method == 'POST'):
        Username = request.form.get('Username')
        Password = request.form.get('Password')
        try:
            user = User.query.filter_by(Username=f'{Username}').all()[0]
            if check_password_hash(user.Password, Password):
                login_user(user)
                return redirect('home')
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
            New_User = User(Username=New_Username, Password=Password_hash, Image_id=random.randint(1, 8))
            db.session.add(New_User)
            db.session.commit()
            return redirect('login')
        elif check_db != []:
            flash('Username is taken')
        elif Password1 != Password2:
            flash('Please check passwords')
        
    return render_template('SignUp_page.html')



@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/login')



                            

if __name__ == '__main__':
    socketio.run(app, host='172.20.10.2', debug=True)
    
    
    
    
    
    

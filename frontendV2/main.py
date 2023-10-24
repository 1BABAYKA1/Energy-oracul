from data import db_session
from forms.user import RegistrationForm, LoginForm, ChangeForm, ChangePasswordForm
from flask_login import LoginManager
from data.users import User
from config import DEBUG, TEMPLATES_AUTO_RELOAD
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, send_file
from flask_mail import Mail, Message
from flask_session import Session
from datetime import datetime, timedelta
from flask import Flask, render_template, redirect, session
from flask_login import LoginManager
import secrets
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import os
from learn.obrabot_learn import start_obrabot_learn as learn
from test_neural.obrabot_test import start_obrabot_test as test
from create.main import add_file as ad
from neural.RF_fit_back import learn as fit
from neural.RF_back import predict
from flask import Flask, request, jsonify, send_from_directory, make_response, send_file
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.config["SECRET_KEY"] = 'LOLLLL'
app.config["DEBUG"] = DEBUG
app.config["TEMPLATES_AUTO_RELOAD"] = TEMPLATES_AUTO_RELOAD

app.config["SESSION_TYPE"] = "filesystem"
Session(app)
app.config["UPLOAD_FOLDER"] = "files/update/"
app.config["PREDICTION_FOLDER"] = "files/predict/"
login = LoginManager(app)

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'flasktest979@gmail.com'
app.config['MAIL_PASSWORD'] = 'bazrnyzucipnnzqg'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)
password_reset_tokens = {}

def generate_token():
    return secrets.token_urlsafe(32)

def send_email(email, text, zaglav):
    msg = Message(zaglav, sender='flasktest979@gmail.com', recipients=[email])
    msg.html = f'{text}'
    mail.send(msg)
    
@login.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)

@app.route('/')
@app.route('/index')
def index():
    if 'user_id' in session:
        user_id = session.get('user_id')
        if user_id:
            db_sess = db_session.create_session()
            user = db_sess.query(User).get(user_id)
            return render_template("menu.html", user=user.name, title='Главная')
    else: 
        return render_template("index.html", title='Главная')


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('expiry', None)
    return redirect('/index')

@app.route('/register', methods=['GET', 'POST'])
def reqister():
    if 'user_id' in session:
        return redirect('/')
    form = RegistrationForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        if form.name.data == '':
            return render_template('register.html', title='Регистрация',
                                    form=form,
                                    message="Имя пользователя не может быть пустым")
        elif form.password.data != form.password_confirm.data:
            return render_template('register.html', title='Регистрация',
                                    form=form,
                                    message="Пароли не совпадают")
        elif len(form.password.data) < 8:
            return render_template('register.html', title='Регистрация',
                                    form=form,
                                    message="Пароли меньше 8 символов!")    

        elif db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                    form=form,
                                    message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        send_email(email=form.email.data, text=f"Дорогой друг, {user.name}!\n Мы благодарим тебя за интерес к нашему сайту.", zaglav='Спасибо за регистрацию')
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)

@app.route("/check_email_work")
def check_email_work():
    try:
        msg = Message("Почта работает", sender = 'flasktest979@gmail.com', recipients = ['wwscxe@yandex.ru'])
        msg.body = "Почтовый сервер успешно работает"
        mail.send(msg)
        return "{status_code : 'work'}"
    except Exception:
        return "{status_code : 'not working'}"

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect('/')
    
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            session['user_id'] = user.id
            session['expiry'] = datetime.now() + timedelta(minutes=15)
            send_email(email=form.email.data, text=f"Дорогой друг, {user.name}!\n Кто-то вошёл в Ваш аккаунт! Если это не Вы, то срочно смените пароль!", zaglav='Уведомление безопасности')
            return redirect("/menu")
        send_email(email=form.email.data, text=f"Дорогой друг, {user.name}!\n Кто-то пытался войти в аккаунт использовая неверный пароль.", zaglav='Уведомление безопасности')
        return render_template('login.html', message="Неправильный логин или пароль", form=form)
    return render_template('login.html', title='Авторизация', form=form)

@app.route('/menu')
def menu():
    user_id = session.get('user_id')
    if user_id:
        db_sess = db_session.create_session()
        user = db_sess.query(User).get(user_id)
        if user:
            session['expiry'] = datetime.now() + timedelta(minutes=15)
            redirect('/')
    return redirect('/login')

@app.route('/change', methods=['GET', 'POST'])
def change():
    if 'user_id' in session:
        return redirect('/')
    form = ChangeForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if not user:
            return render_template('change.html', title='Смена пароля',
                                    form=form,
                                    message="Пользователь не найден")
        else:
            token = generate_token()
            email = form.email.data
            password_reset_tokens[email] = token
            send_email(
                email=email,
                text=f"{render_template('email/reset_password.html', user=User.name, token=token)}",
                zaglav='Уведомление безопасности'
            )
            return redirect('/')
    return render_template('change.html', title='Забыл пароль', form=form)

@app.route('/change_password?token=<token>', methods=['GET', 'POST'])
def change_password(token):
    if 'user_id' in session:
        return redirect('/')
    email = next((email for email, t in password_reset_tokens.items() if t == token), None)
    print(email)
    print(password_reset_tokens)
    if email:
        form = ChangePasswordForm()
        if form.validate_on_submit():
            db_sess = db_session.create_session()
            user = db_sess.query(User).filter(User.email == email).first()
            if user:
                user.set_password(form.password.data)
                db_sess.commit()
                del password_reset_tokens[email]
                return redirect('/')
        return render_template('changepassword.html', title='Смена пароля', form=form)
    return redirect('/')

@app.route('/upload', methods=['POST'])
def upload_file():
    response_data = {}
    good = {"status_code": "success"}
    error_code = {"status_code": "error"}
    error_format = {"status_code": "format_error"}
    if request.method == 'POST':
        
        for key, value in request.args.items():
            response_data[key] = value
        print(response_data['hours'])
        f = request.files['file']
        filename = secure_filename(f.filename)
        hours = response_data['hours']
        longitude = response_data['longitude']
        latitude = response_data['latitude']
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        
        file = open(os.path.join(app.config['UPLOAD_FOLDER'], filename), "r")
        first_line = file.readline().strip()  
        expected_header = "time;target;date"

        if first_line == expected_header:
            ad(filename, hours)
            learn(filename, latitude, longitude)
            test(filename, latitude, longitude, hours)
            # fit(filename)
            return jsonify({'status_code': 'good', 'url': predict(filename, hours)})
        else:
            return jsonify(error_format)
    else:
        return jsonify(error_code)
    
@app.route('/download/files/predict/<filename>', methods=['GET'])
def download_prediction(filename):
    response = make_response(send_file(os.path.join(app.config['PREDICTION_FOLDER'], filename)))
    response.headers['Content-Disposition'] = f'attachment; filename=Predict.xlsx'
    return response


def main():
    db_session.global_init("db/users.db")
    app.run(port=8080, host='127.0.0.1')


if __name__ == '__main__':
    main()

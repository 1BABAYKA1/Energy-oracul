from data import db_session
from forms.user import RegistrationForm, LoginForm
from flask_login import login_required, LoginManager, logout_user
from data.users import User
from config import DEBUG, TEMPLATES_AUTO_RELOAD
from flask import Flask, render_template, redirect, session

app = Flask(__name__)
app.config["DEBUG"] = DEBUG
app.config["DEBUG"] = TEMPLATES_AUTO_RELOAD

login = LoginManager(app)
app.config["SECRET_KEY"] = 'Energy_Oracul'


@login.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)

@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html", title='Главная')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegistrationForm()
    if form.validate_on_submit():
        if form.password.data != form.password_confirm.data:
            return render_template('register.html', title='Регистрация',
                                    form=form,
                                    message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
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
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            session['user_id'] = user.id
            return redirect("/menu")
        return render_template('login.html', message="Неправильный логин или пароль", form=form)
    return render_template('login.html', title='Авторизация', form=form)

@app.route('/menu')
def menu():
    user_id = session.get('user_id')
    if user_id:
        db_sess = db_session.create_session()
        user = db_sess.query(User).get(user_id)
        if user:
            return render_template('menu.html', user=user.name, title='Меню')
    
    return redirect('/login')


@app.route('/about')
def about():
    return render_template('about.html', title='О проекте')


def main():
    db_session.global_init("db/users.db")
    app.run(port=8080, host='127.0.0.1')


if __name__ == '__main__':
    main()

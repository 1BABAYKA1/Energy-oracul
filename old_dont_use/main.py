from flask import Flask, render_template, redirect
from data import db_session
from flask_login import login_required, LoginManager, logout_user
from data.users import User
from config import DEBUG, TEMPLATES_AUTO_RELOAD
from flask_babelex import Babel
from forms.user import RegistrationForm, LoginForm

app = Flask(__name__)
app.config["SECRET_KEY"] = 'OpOp'
app.config["DEBUG"] = DEBUG
app.config["TEMPLATES_AUTO_RELOAD"] = TEMPLATES_AUTO_RELOAD
babel = Babel(app)
login = LoginManager(app)


@login.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)

@app.route('/')
@app.route('/index')
def index():
    return render_template("main.html", title='Главная')

@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegistrationForm()
    if form.validate_on_submit():
        if form.password.data != form.password_confirm.data:
            return render_template('register.html', title='Регистрация',
                                    form=form)
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                    form=form)
        user = User(
            name=form.name.data,
            email=form.email.data,
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            return redirect("/get_bot")
        return render_template('login.html',
                               title='Авторизация',
                                form=form)
    return render_template('login.html', title='Авторизация', form=form)

@app.route('/get_bot')

def get_bot():
    return render_template('bot.html')


def main():
    db_session.global_init("db/users.db")
    app.run(port=8080, host='127.0.0.1')


if __name__ == '__main__':
    main()




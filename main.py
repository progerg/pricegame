from flask_login import login_user, LoginManager, login_manager, login_required, logout_user, current_user
from data import Game
from data.db_session import *
from data.users import User, EditForm, RegisterForm, LoginForm
import flask
from flask import Flask, render_template, redirect, request, url_for, flash, make_response

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hello'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_message == 'Авторизуйтесь для доступа к закрытым страницам'


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/games', methods=['GET', 'POST'])
def games():
    games_list = db_sess.query(Game.Game).all()
    if 'up' == flask.request.form.get('price'):
        games_list = db_sess.query(Game.Game).order_by(Game.Game.st_price).all()
    else:
        games_list = db_sess.query(Game.Game).order_by(-Game.Game.st_price).all()
    return flask.render_template('games.html', games=games_list)


@login_required
@app.route('/follow/<int:id>', methods=['GET', 'POST'])
def follow(id):
    print(id)
    current_user.foll_games = id
    db_sess.merge(current_user)
    db_sess.commit()
    return redirect(url_for('games'))


@login_required
@app.route('/unfollow/<int:id>', methods=['GET', 'POST'])
def unfollow(id):
    print(id)
    current_user.foll_games = None
    db_sess.merge(current_user)
    db_sess.commit()
    return redirect(url_for('profile'))


@login_manager.user_loader
def load_user(user_id):
    db_sess = create_session()
    return db_sess.query(User).get(user_id)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        global_init('db/game.db')
        db_sess = create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect(url_for('index'))
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
            age=form.age.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect(url_for('login'))
    return render_template('register.html', title='Регистрация', form=form)


@login_required
@app.route('/profile_edit', methods=['GET', 'POST'])
def profile_edit():
    form = EditForm()
    if request.method == "GET":
        form.email.data = current_user.email
        form.name.data = current_user.name
    if form.validate_on_submit():
        if current_user.check_password(form.old_password.data) or form.new_password.data == '':
            f = form.avatar.data
            current_user.name = form.name.data
            current_user.email = form.email.data
            current_user.age = form.age.data
            current_user.password = form.new_password.data
            current_user.profile_photo = f.read()
            db_sess.merge(current_user)
            db_sess.commit()
            return redirect(url_for('profile'))
        flash('Неправильный пароль')
        return render_template('profile_edit.html', title='Edit Profile', form=form)
    return render_template('profile_edit.html', title='Edit Profile', form=form)


@app.route('/user_avatar/id<int:id>')
@login_required
def user_avatar(id):
    db_sess = create_session()
    img = db_sess.query(User).filter(User.id == id).first().profile_photo
    if not img:
        return ""
    h = make_response(img)
    return h


@login_required
@app.route('/profile', methods=['GET', 'POST'])
def profile():
    foll_games = current_user.foll_games
    games_list = db_sess.query(Game.Game).filter((Game.Game.id == foll_games)).all()
    return render_template('profile.html', title='Profile', games=games_list)


if __name__ == '__main__':
    global_init('db/game.db')
    db_sess = create_session()
    app.run(port=8080, host='127.0.0.1')

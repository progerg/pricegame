from flask_login import login_user, LoginManager, login_manager, login_required, logout_user, current_user
from data.Game import Game
from data.EGSGameData import EGSGameData
from data.SteamGameData import SteamGameData
from data.db_session import *
from data.users import User, EditForm, RegisterForm, LoginForm
import flask
from flask import Flask, render_template, redirect, request, url_for, flash, make_response
from os.path import dirname, join
from flask_caching import Cache
from json import loads

app = Flask(__name__, static_folder=join(dirname(__file__), 'static'))
app.config['SECRET_KEY'] = 'hello'

cache = Cache(config={"CACHE_TYPE": "SimpleCache", "CACHE_DEFAULT_TIMEOUT": 60})
cache.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_message = 'Авторизуйтесь для доступа к закрытым страницам'


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    if flask.request.method == 'POST':
        cache.set('name', flask.request.form.get('game_name'))
        return redirect('/games')
    return render_template('index.html')


@app.route('/games', methods=['GET', 'POST'])
@app.route('/games/<int:page>', methods=['GET', 'POST'])
def games(page=1):
    last_page = first_page = False
    query = db_sess.query(Game)
    if flask.request.method == 'POST':
        cache.set('name', flask.request.form.get('name'))
        if flask.request.form.get('price') == 'up':
            cache.set('price_up', True)
        else:
            cache.set('price_up', False)
        return redirect('/games')

    if cache.get('name'):
        name = cache.get('name')
        query = query.filter(Game.name.like(f'%{name}%'))

    len_games_list = query.count()

    if page <= 0:
        return redirect('/games')
    elif page > len_games_list // 15 + 1:
        page = len_games_list // 15 + 1
        return redirect(f'/games/{page}')
    elif page == 1:
        first_page = True
    elif page == len_games_list // 15 + 1:
        last_page = True

    if cache.get('price_up'):
        games_list = list(query.order_by(Game.min_price).limit(15).offset(15 * (page - 1)))
    else:
        games_list = list(query.order_by(-Game.min_price).limit(15).offset(15 * (page - 1)))
    return render_template('games.html', games=games_list, price_up=cache.get('price_up'), name=cache.get('name'),
                           page=page, first_page=first_page, last_page=last_page)


@app.route('/game/<int:game_id>')
def game(game_id: int):
    game = db_sess.query(Game).filter(Game.id == game_id).first()
    imgs = dlcs = metacritic = None
    if game:
        if game.steam_game:
            if game.steam_game.screenshots:
                imgs = loads(game.steam_game.screenshots)
            if game.steam_game.dlc:
                dlcs = game.steam_game.dlc
            if game.steam_game.metacritic:
                metacritic = loads(game.steam_game.metacritic)
        return render_template('game.html', game=game, dlcs=dlcs, imgs=imgs, metacritic=metacritic)
    return f'Game with id {game_id} doesn`t exists'


@login_required
@app.route('/follow/<int:id>', methods=['GET', 'POST'])
def follow(id):
    print(id)
    if current_user.foll_games:
        foll_games = current_user.foll_games.split()
    else:
        foll_games = []
    print(foll_games)
    if foll_games and str(id) not in foll_games:
        current_user.foll_games = f'{current_user.foll_games}, {id}'
    elif str(id) in foll_games:
        flash('You are already following this game')
    else:
        current_user.foll_games = f'{id}'
    game = db_sess.query(Game).filter(Game.id == id).first()
    if game.foll_profiles:
        profiles = game.foll_profiles.split()
    else:
        profiles = []
    if profiles and str(current_user.id) not in profiles:
        game.foll_profiles = f'{game.foll_profiles}, {current_user.id}'
    else:
        game.foll_profiles = f'{current_user.id}'
    db_sess.merge(current_user)
    db_sess.commit()
    return redirect(url_for('games'))


@login_required
@app.route('/unfollow/<int:id>', methods=['GET', 'POST'])
def unfollow(id):
    print(id)
    foll_games = current_user.foll_games.split(', ')
    foll_games.remove(str(id))
    foll_games = ', '.join(foll_games)
    current_user.foll_games = foll_games
    game = db_sess.query(Game).filter(Game.id == id).first()
    profiles = game.foll_profiles.split(', ')
    profiles.remove(str(current_user.id))
    game.foll_profiles = ', '.join(profiles)
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
            age=form.age.data,
            profile_photo=open('static/img/no_avatar.png', 'rb').read()
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


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')


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
    if current_user.foll_games:
        foll_games = current_user.foll_games.split(', ')
        foll_games = list(map(lambda x: int(x), foll_games))
        games_list = db_sess.query(Game).filter(Game.id.in_(foll_games)).all()
    else:
        games_list = []
    return render_template('profile.html', title='Profile', games=games_list)


if __name__ == '__main__':
    global_init('db/games.db')
    db_sess = create_session()
    app.run(port=8080, host='127.0.0.1')

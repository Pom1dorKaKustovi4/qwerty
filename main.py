import shutil

from flask import Flask, render_template, redirect, request, abort
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
import requests

# from data import db_session
from data import db_session
from data.cart import Cart
from data.users import User
from forms.user import LoginForm, RegisterForm

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    znachok = "static/img/znachok.png"
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают", znachok=znachok)
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть", znachok=znachok)
        user = User(
            email=form.email.data,
            user_name=form.name.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form, znachok=znachok)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    znachok = "static/img/znachok.png"
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form, znachok=znachok)
    return render_template('login.html', title='Авторизация', form=form, znachok=znachok)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route("/payment")
def payment():
    return render_template('payment.html')


@app.route('/')
@app.route('/funny_price')
@app.route('/funny_price/<int:page>', methods=['GET', 'POST'])
def index(page=1):
    id = 1 + (page - 1) * 8
    db_sess = db_session.create_session()
    session = db_sess.query(Cart)
    links = []
    for i in range(8):
        links.append([session.filter(Cart.id == id + i).first().links, session.filter(Cart.id == id + i).first().name,
                      session.filter(Cart.id == id + i).first().description])
    znachok = "static/img/znachok.png"
    logo = "static/img/ico/logo.jpg"
    if current_user.is_authenticated:
        userr = current_user.user_name
        logo = f"static/img/ico/{userr}.jpg"
    return render_template('up_menu.html', title='Смешные цены',
                           a=links[0][0], b=links[1][0], c=links[2][0], d=links[3][0], e=links[4][0],
                           f=links[5][0], g=links[6][0], h=links[7][0], ico=logo, znachok=znachok,
                           name1=links[0][1], name2=links[1][1], name3=links[2][1], name4=links[3][1],
                           name5=links[4][1],
                           name6=links[5][1], name7=links[6][1], name8=links[7][1], page=page)


@app.route('/info')
def info():
    znachok = "static/img/znachok.png"
    return render_template('info.html', title="Информация", znachok=znachok)


@app.route('/game/<id>', methods=['GET', 'POST'])
def product_add(id):
    page = int(id[1:])
    id = int(id[0]) + (page - 1) * 8
    logo = "static/img/ico/logo.jpg"
    znachok = "../../static/img/znachok.png"
    db_sess = db_session.create_session()
    session = db_sess.query(Cart).filter(Cart.id == id).first()
    price = [session.price_steam, session.price_egs, session.price_gog]
    best_name = ""
    best_prise = 0
    if isinstance(price[0], int) and price[0] == min(price):
        best_name = "Steam"
        best_prise = str(price[0]) + " руб."
    elif isinstance(price[1], int) and price[1] == min(price):
        best_name = "EGS"
        best_prise = str(price[1]) + " руб."
    elif isinstance(price[2], int) and price[2] == min(price):
        best_name = "GOG"
        best_prise = str(price[2]) + " руб."
    for i in range(3):
        if price[i] == 99999999999:
            price[i] = "не продаётся"
        else:
            price[i] = str(price[i]) + " руб."
    if current_user.is_authenticated:
        userr = current_user.user_name
        logo = f"../static/img/ico/{userr}.jpg"
    return render_template('info.html', title="Информация", znachok=znachok, ico=logo, name=session.name,
                           description=session.description, price_steam=price[0], best_prise=best_prise,
                           price_egs=price[1], price_gog=price[2], best_name=best_name)


@app.route('/input')
def loading_of_picture():
    return render_template('input.html')


@app.route('/inputt', methods=['GET', 'POST'])
def picture():
    f = request.files['file']
    with open(f'static/img/ico/{current_user.user_name}.jpg', 'wb') as file:
        shutil.copyfileobj(f, file)
    return redirect("/")


if __name__ == "__main__":
    db_session.global_init("users.db")
    app.run(port=8080, host='127.0.0.1')

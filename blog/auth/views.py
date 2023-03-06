from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import logout_user, login_user, login_required
from werkzeug.security import check_password_hash

auth = Blueprint('auth', __name__, url_prefix='/auth', static_folder='../static')


@auth.route('/login', methods=["GET", "POST"])
def login():
    # Если в реквесте метод равен GET, то отрисовываем шаблон
    if request.method == 'GET':
        return render_template(
            'auth/login.html',
        )

    email = request.form.get('email')  # Получаем данные из формы
    password = request.form.get('password')

    from blog.models import User

    user = User.query.filter_by(email=email).first()  # ищем юзера по фильтру

    if not user or not check_password_hash(user.password, password):  # Если нет такого юзера или хеш пароля не совпал
        # (передаём для сравнения имеющийся в БД пароль и передаваемый)
        flash('Check your login details')  # flash - это ф-ия, которя умеет на фронтенд через сессию прокидывать
        # сообщения
        return redirect(url_for('.login'))  # редирект, если ошибка

    login_user(user)
    return redirect(url_for('user.profile', pk=user.id))  # Если прошла авторизация


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('.login'))

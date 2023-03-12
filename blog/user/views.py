# Реализация blueprint - пользователи
from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_required, current_user, login_user
from werkzeug.exceptions import NotFound
from werkzeug.security import generate_password_hash

from blog.app import login_manager
from blog.extensions import db
from blog.forms.users import UserRegisterForm
from blog.models import User

user = Blueprint('user', __name__, url_prefix='/users', static_folder='../static')  # user - name,
# __name__ - текущее название пакета, static_folder - где хранится статика
# USERS = {
#     1: "James",
#     2: "Brian",
#     3: "Peter",
# }
# USERS = ['Alice', 'John', 'Mike']


@user.route('register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('user.profile', pk=current_user.id))

    form = UserRegisterForm(request.form)
    errors = []
    if request.method == 'POST' and form.validate_on_submit():
        if User.query.filter_by(email=form.email.data).count():
            form.email.errors.append('Email error')
            return render_template('users/register.html', form=form)

        _user = User(
            email=form.email.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            password=generate_password_hash(form.password.data),
        )

        db.session.add(_user)
        db.session.commit()

        login_user(_user)  # Авторизация после регистрации

    return render_template(
        'users/register.html',
        form=form,
        errors=errors,
    )


@user.route('/')  # регистрируем в роуте блюпринт по адресу localhost/user/ с функцией ниже:
def user_list():  # ф-ия, которая не принимает ничего
    from blog.models import User
    users = User.query.all()
    return render_template(  # Ф-ия render_template принимает в себя template name или list
        # (название нашего шаблона, который должен быть отрисован)
        'users/list.html',
        users=users,
    )


@user.route('/<int:pk>')  # pk - primary key
@login_required
def profile(pk: int):  # Принимает id юзера
    """Получение конкретного юзера"""
    from blog.models import User

    _user = User.query.filter_by(id=pk).one_or_none()  # Получаем конкретного юзера через фильтр по параметр, и
    # используем метод, который либо возвращает 1 элемент из выборки или none
    return render_template(
        'users/profile.html',
        user=_user,
    )

# Закоментил первую часть 3-го урока:
# @user.route('/<int:pk>')  # pk - primary key
# def get_user(pk: int):  # Принимает id юзера
#     """Получение конкретного юзера"""
#     from blog.models import User
#     _user = User.query.filter_by(id=pk).one_or_none()  # Получаем конкретного юзера через фильтр по параметр, и
#     # используем метод, который либо возвращает 1 элемент из выборки или none
#     return render_template(
#         'users/profile.html',
#         user=_user,
#     )


# Закомментировал первоначальный вариант работы с юзерами
# @user.route('/')  # регистрируем в роуте блюпринт по адресу localhost/user/ с функцией ниже:
# def user_list():  # ф-ия, которая не принимает ничего
#     return render_template(  # Ф-ия render_template принимает в себя template name или list
#         # (название нашего шаблона, который должен быть отрисован)
#         'users/list.html',
#         users=USERS,
#     )


# @user.route('/<int:pk>')  # pk - primary key
# def get_user(pk: int):  # Принимает id юзера
#     """Получение конкретного юзера"""
#     try:  # обрабатываем исключение, если юзера с таким id не будет
#         user_name = USERS[pk]
#     except KeyError:
#         raise NotFound(f'User id {pk} not found')  # Выдаём текст с отработанной ошибкой
#         # return redirect('/users/')  # В случае ошибки - редиректим на указанный адрес
#     user_pk = pk
#     return render_template(
#         'users/profile.html',
#         user_name=user_name,
#         user_pk=user_pk,
#     )
